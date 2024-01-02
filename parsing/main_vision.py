import Quartz
from Foundation import NSURL, NSRange
import Vision
from PIL import Image, ImageDraw


def recognize_text_handler(request, error):
    observations = request.results()
    results = []
    for observation in observations:
        recognized_text = observation.topCandidates_(1)[0]
        
        box_range = NSRange(0, len(recognized_text.string()))
        boxObservations = recognized_text.boundingBoxForRange_error_(box_range, None)

        boundingBox = boxObservations[0].boundingBox()

        image_width, image_height = input_image.extent().size.width, input_image.extent().size.height
        rect = Vision.VNImageRectForNormalizedRect(boundingBox, image_width, image_height)

        results.append([recognized_text.string(), recognized_text.confidence(), rect])

    for result in results:
        print(result[0])

    visualize_results(results)


def visualize_results(results):
    image = Image.open(img_path)
    draw=ImageDraw.Draw(image)
    for result in results:
        rect = result[-1]
        min_x = Quartz.CGRectGetMinX(rect)
        max_x = Quartz.CGRectGetMaxX(rect)
        max_y = input_image.extent().size.height - Quartz.CGRectGetMinY(rect)
        min_y = input_image.extent().size.height - Quartz.CGRectGetMaxY(rect)
        draw.rectangle([(min_x,min_y),(max_x,max_y)],outline="black",width=3)
    image.show()


#img_path = "/Users/christianreetz/Desktop/Screenshot 2023-12-31 at 11.54.24 AM.png"
img_path = "/Users/christianreetz/Downloads/3page.pdf"

input_url = NSURL.fileURLWithPath_(img_path)
input_image = Quartz.CIImage.imageWithContentsOfURL_(input_url)

request_handler = Vision.VNImageRequestHandler.alloc().initWithCIImage_options_(
        input_image, None
)
request = Vision.VNRecognizeTextRequest.alloc().initWithCompletionHandler_(recognize_text_handler)

error = request_handler.performRequests_error_([request], None)

request_handler.dealloc()
request.dealloc()




