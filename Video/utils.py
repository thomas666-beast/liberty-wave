import tempfile

from moviepy import VideoFileClip


def generate_thumbnail_from_video(video_path):
    """
    Generate a thumbnail from a video file by extracting a frame at 25% of the video duration
    using MoviePy.
    """
    try:
        # Open the video file
        clip = VideoFileClip(video_path)

        # Get the frame at 25% of the video duration
        frame_time = clip.duration * 0.25

        # Get the frame
        frame = clip.get_frame(frame_time)

        # Create a temporary file for the thumbnail
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        temp_path = temp_file.name
        temp_file.close()

        # Save the frame as an image using MoviePy's built-in method
        clip.save_frame(temp_path, t=frame_time)

        # Close the clip
        clip.close()

        return temp_path
    except Exception as e:
        # Log the error and re-raise
        print(f"Error generating thumbnail from video: {e}")
        raise
