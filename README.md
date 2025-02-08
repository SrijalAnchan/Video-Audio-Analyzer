
# Video and Audio Analyzer Tool

This is a Flask web application designed to analyze video files for common issues such as blank screens, blurry frames, frame errors, white space, and audio drops. The results are displayed in a user-friendly interface, and a detailed PDF report can be generated.

## Features
- **File Upload**: Upload video files (up to 100 MB) for analysis.
- **Analysis Options**:
  - **Blank Screen Detection**: Detects sections of a video containing blank screens.
  - **Blur Detection**: Identifies blurry frames in the video.
  - **Frame Error Detection**: Highlights frames with significant visual artifacts or errors.
  - **White Space Detection**: Finds frames with excessive white or empty space.
  - **Audio Drop Detection**: Identifies silent or muted portions in the video.
- **Issue Navigation**: Click on detected issues to jump directly to the corresponding frame in the video.
- **Detailed Results**: Analysis results are displayed interactively on the web interface.
- **PDF Report**: Generate and download a summary report of the analysis.

## Technologies Used
- **Flask**: For building the web application.
- **OpenCV**: For video processing and frame analysis.
- **Librosa**: For audio analysis and silence detection.
- **NumPy**: For numerical computations.
- **ReportLab**: For creating PDF reports.
- **HTML/CSS/JavaScript**: For building the front-end user interface.

---

#### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/SrijalAnchan/Video-Audio-Analyzer.git
   cd video-audio-analysis-app
   ```

2. Create the necessary directories:
   ```bash
   mkdir uploads
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

---

#### Usage
1. **Upload a Video**: Use the web interface to upload a video file.
2. **Select Analysis Type**:
   - **Blank Screen Detection**: Detects blank sections in the video.
   - **Blur Detection**: Identifies blurry frames.
   - **Frame Error Detection**: Highlights visual errors in frames.
   - **Audio Drop Detection**: Locates silent sections in the audio.
3. **Explore Results**: View identified issues and click on them to navigate directly to the relevant frame in the video.

---

#### Project Structure
```
├── app.py               # Main Flask application
├── templates/           # HTML templates for the web interface
├── static/              # Static files (CSS, JS, and user uploads)
│   └── uploads/         # Folder for uploaded files
```
