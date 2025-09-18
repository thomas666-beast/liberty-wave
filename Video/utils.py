import tempfile

import cv2


def generate_thumbnail_from_video(video_path):
    """
    Generate a thumbnail from a video file by extracting a frame at 25% of the video duration
    """
    try:
        # Open the video file
        cap = cv2.VideoCapture(video_path)

        # Get total frames and set position to 25% of the video
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_pos = int(total_frames * 0.25)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)

        # Read the frame
        success, frame = cap.read()
        cap.release()

        if not success:
            # If failed to read at 25%, try the first frame
            cap = cv2.VideoCapture(video_path)
            success, frame = cap.read()
            cap.release()
            if not success:
                raise Exception("Could not read video frame")

        # Create a temporary file for the thumbnail
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        temp_path = temp_file.name
        temp_file.close()

        # Save the frame as an image
        cv2.imwrite(temp_path, frame)

        return temp_path
    except Exception as e:
        # Log the error and re-raise
        print(f"Error generating thumbnail from video: {e}")
        raise
