import os
import numpy as np
import cv2
import random
import argparse


def transform_image(image):
    height, width, _ = image.shape

    start_range = 0
    end_range = min(height, width) // 2.5
    pts1 = np.float32([[0, 0], [width - 1, 0], [0, height - 1], [width - 1, height - 1]])
    pts2 = np.float32([[np.random.randint(start_range, end_range), np.random.randint(start_range, end_range)],
                       [width - 1 - np.random.randint(start_range, end_range), np.random.randint(start_range, end_range)],
                       [np.random.randint(start_range, end_range), height - 1 - np.random.randint(start_range, end_range)],
                       [width - 1 - np.random.randint(start_range, end_range), height - 1 - np.random.randint(start_range, end_range)]])

    M = cv2.getPerspectiveTransform(pts1, pts2)
    image = cv2.warpPerspective(image, M, (width, height))
    return image


def augment_dataset(dataset_path):
    split = ['train', 'val']

    count = 0
    total = len(os.listdir(f'{dataset_path}/images/{split}'))
    for file in os.listdir(f'{dataset_path}/images/{split}').copy():
        file_name = file.split('.')[0]
        count += 1
        print(f'{count} / {total}')

        file_dir = f'{dataset_path}/images/{split}/{file}'
        label_dir = f'{dataset_path}/labels/{split}/{file_name}.txt'
        if not os.path.isfile(label_dir):
            print(file_dir)
            os.remove(file_dir)
            continue

        img = cv2.imread(file_dir)
        height, width, _ = img.shape

        # Read label
        with open(label_dir, 'r') as fr:
            data = fr.readlines()

        # Transform image
        img = transform_image(img)

        new_data = ''
        for line in data:
            label = line.strip().split(' ')[0]
            x, y, w, h = line.strip().split(' ')[1:]
            x = int(float(x) * width)
            y = int(float(y) * height)
            w = int(float(w) * width)
            h = int(float(h) * height)

            # Compute 4 origin points
            x0 = x - w//2
            y0 = y - h//2
            x1 = x + w//2
            y1 = y + h//2

            point1 = [x0, y0]
            point2 = [x1, y0]
            point3 = [x1, y1]
            point4 = [x0, y1]

            points = np.array([point1, point2, point3, point4])
            # print(points)

            # img = cv2.rectangle(img, (x0, y0), (x1, y1), color=(255, 0, 0), thickness=3)

            # Compute new bounding box
            points = points.astype(np.float32).reshape(-1, 1, 2)
            transformed_points = cv2.perspectiveTransform(points, M)
            transformed_points = transformed_points.astype(int)
            # print(transformed_points)

            x0_transform = min(transformed_points[:, :, 0])[0]
            y0_transform = min(transformed_points[:, :, 1])[0]
            x1_transform = max(transformed_points[:, :, 0])[0]
            y1_transform = max(transformed_points[:, :, 1])[0]

            x_transform = ((x0_transform + x1_transform) / 2) / width
            y_transform = ((y0_transform + y1_transform) / 2) / height
            w_transform = (x1_transform - x0_transform) / width
            h_transform = (y1_transform - y0_transform) / height

            # img = cv2.rectangle(img, (x0_transform, y0_transform), (x1_transform, y1_transform), color=(0, 255, 0), thickness=3)

            # Write data
            new_data += str(label) + ' ' + ' '.join([str(x_transform), str(y_transform), str(w_transform), str(h_transform)]) + '\n'

        new_data = new_data.strip()
        cv2.imwrite(f'{dataset_path}/images/{split}/{file_name}_rotate.jpg', img)
        with open(f'{dataset_path}/labels/{split}/{file_name}_rotate.txt', 'w') as fw:
            fw.write(new_data)

        # cv2.imshow('IMG', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # if count == 3:
        #     break


if __name__ == '__main__':
    # ADD ARGPARSE
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--dataset', required=True, help='path to training dataset')
    args = ap.parse_args()

    augment_dataset(args.dataset)