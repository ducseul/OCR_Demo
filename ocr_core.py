import cv2
import pytesseract
from point import Boundary_Point

def draw_boundary(im2, x, y, w, h):
    font_scale = 0.3
    # top left point
    cv2.circle(im2, (x, y), 2, (0, 0, 255), 2)
    cv2.putText(im2, join_tup((x, y)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0), 1, cv2.LINE_AA)
    # bottom right point
    cv2.circle(im2, (x + w, y + h), 2, (0, 0, 255), 2)
    cv2.putText(im2, join_tup((x + w, y + h)),(x + w, y + h), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0), 1, cv2.LINE_AA)
    # middle point
    cv2.circle(im2, Boundary_Point((x, y), (x + w, y + h)).get_mid_point(), 2, (0, 0, 255), 2)
    cv2.putText(im2, join_tup(Boundary_Point((x, y), (x + w, y + h)).get_mid_point()),Boundary_Point((x, y), (x + w, y + h)).get_mid_point(), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0), 1, cv2.LINE_AA)

# helpr_fnc
def join_tup(tup):
    res = str(tup[0])
    for idx in tup[1:]:
        res = res + "-" + str(idx)
    return res

def sort_contours_as_x(contours, img):
    # create index for contours
    point_entries = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # print((x, y), (x + w, y + h))
        point_entry = Boundary_Point((x, y), (x + w, y + h))
        point_entries.append(((point_entry.coord_tl, point_entry.coord_br), point_entry.get_mid_point()[1], cnt))
        # print(point_entry.get_mid_point())

    # sorting point_entries
    point_entries.sort(reverse=False, key=lambda x:x[1])
    tmp = []
    for point in point_entries:
        if not (point[0][0] == (0, 0) and point[0][1] == (img.shape[1], img.shape[0])):
            tmp.append(point[2])
        else:
            # drop this frame due to it's being size of full img => miscropped
            # print("drop 0x00")
            pass

    return tmp

def img2text(img):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    # Read image from which text needs to be extracted
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_NONE)

    draw_bound_img = img.copy()
    ocr_crop_img = gray.copy()
    file = open("output.txt", "w+")
    file.write("")
    file.close()

    print("Found", len(contours), " section")

    contours = sort_contours_as_x(contours, img)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cropped = ocr_crop_img[y:y + h, x:x + w]
        text = pytesseract.image_to_string(cropped)

        rect = cv2.rectangle(draw_bound_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        draw_boundary(draw_bound_img, x, y, w, h)
            
        file = open("output.txt", "a")
        file.write(text)
        print(text)
        file.write("\n")
        file.close

    # show the origin clone img has been boundaried
    cv2.imshow("drawing", draw_bound_img)
    #show each part of boundary
    # for cnt in contours:
    #     x, y, w, h = cv2.boundingRect(cnt)
    #     cropped = ocr_crop_img[y:y + h, x:x + w]
    #     rect = cv2.rectangle(draw_bound_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #     draw_boundary(draw_bound_img, x, y, w, h)
    #     while True:
    #         cv2.imshow(join_tup(((x, y), (x + w, y + h))), cropped)
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break
    
    return "txt"
