
from bike_fit_app.videoAnalyse import VideoAnalyzer


def test_should_accept_only_video_formats():


    # todo: descobrir como testar se levanta um erro
    try:
        video_analizer = VideoAnalyzer("path_to_some_png.png") # deve fazer um raise Exception
        assert False
    except Exception:
        assert True


    
    frame = video_analizer.process_next_frame()
    frame is not None


