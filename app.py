from flask import Flask, render_template, request, url_for
import os
import cv2
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

# Get the sample style sheet to style the PDF content
styles = getSampleStyleSheet()

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'  # Store videos in static/uploads
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def analyze_video(video_path):
    issues = []
    issue_count = {
        'frame_drop': 0,
        'blank_frame': 0,
        'blurry_frame': 0
    }

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    prev_frame = None
    for i in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            issues.append({
                'type': 'frame_drop',
                'timestamp': i / fps
            })
            issue_count['frame_drop'] += 1
            continue

        if prev_frame is not None:
            diff = cv2.absdiff(frame, prev_frame)
            if np.mean(diff) < 5:
                issues.append({
                    'type': 'blank_frame',
                    'timestamp': i / fps
                })
                issue_count['blank_frame'] += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.Laplacian(gray, cv2.CV_64F).var()
        if blur < 100:
            issues.append({
                'type': 'blurry_frame',
                'timestamp': i / fps
            })
            issue_count['blurry_frame'] += 1

        prev_frame = frame

    return issues, issue_count

@app.route('/', methods=['GET', 'POST'])
def index():
    video_file = None
    if request.method == 'POST':
        video_file = request.files['video_file']
        if video_file:
            video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
            video_file.save(video_path)

            issues, issue_count = analyze_video(video_path)
            pdf_path = os.path.join('static', 'uploads', 'report.pdf')
            generate_pdf_report(issues, pdf_path,issue_count)

            return render_template('index.html', issues=issues, issue_count=issue_count, pdf_path=pdf_path, video_file=video_file.filename)

    return render_template('index.html', video_file=video_file)

def generate_pdf_report(issues, pdf_path, issue_count):
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []

    # Add a title
    elements.append(Paragraph("<b>Video Analysis Report</b>", styles['Heading1']))

    # Add issue counts at the beginning
    issue_summary = f"""
    <b>Frame Drops:</b> {issue_count['frame_drop']}<br/>
    <b>Blank Frames:</b> {issue_count['blank_frame']}<br/>
    <b>Blurry Frames:</b> {issue_count['blurry_frame']}<br/>
    """
    elements.append(Paragraph(issue_summary, styles['Normal']))

    # If there are issues, create a table
    if issues:
        data = [['Timestamp', 'Issue Type']]  # Table header
        for issue in issues:
            data.append([f"{issue['timestamp']:.2f} seconds", issue['type']])

        # Create and style the table
        table = Table(data, colWidths=[100, 250])  # Adjust column widths for better formatting
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LINEBEFORE', (0, 0), (0, -1), 1, colors.black),
            ('LINEAFTER', (-1, 0), (-1, -1), 1, colors.black)
        ])
        table.setStyle(table_style)

        elements.append(table)
    else:
        # If no issues were found, add a message indicating that
        elements.append(Paragraph("No issues detected in the video.", styles['Normal']))

    doc.build(elements)

if __name__ == '__main__':
    app.run(debug=True)
