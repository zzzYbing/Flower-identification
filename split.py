import os
import random
import shutil

def data_set_split(src_data_folder, target_data_folder, train_val_scale=0.9, test_scale=0.1):
    '''
    读取源数据文件夹，生成划分好的文件夹，分为train_val和test两个文件夹进行
    :param src_data_folder: 源文件夹路径
    :param target_data_folder: 目标文件夹路径
    :param train_val_scale: 训练验证集比例
    :param test_scale: 测试集比例
    :return:
    '''
    print("开始数据集划分")
    class_names = [folder for folder in os.listdir(src_data_folder) if os.path.isdir(os.path.join(src_data_folder, folder))]

    # 在目标目录下创建文件夹
    split_names = ['train_val', 'test']
    for split_name in split_names:
        split_path = os.path.join(target_data_folder, split_name)
        if not os.path.exists(split_path):
            os.makedirs(split_path)
        # 在split_path的目录下创建类别文件夹
        for class_name in class_names:
            class_split_path = os.path.join(split_path, class_name)
            if not os.path.exists(class_split_path):
                os.makedirs(class_split_path)

    # 按照比例划分数据集，并进行数据图片的复制
    for class_name in class_names:
        current_class_data_path = os.path.join(src_data_folder, class_name)
        current_all_data = [file for file in os.listdir(current_class_data_path) if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png')]
        current_data_length = len(current_all_data)
        current_data_index_list = list(range(current_data_length))
        random.shuffle(current_data_index_list)

        train_val_folder = os.path.join(os.path.join(target_data_folder, 'train_val'), class_name)
        test_folder = os.path.join(os.path.join(target_data_folder, 'test'), class_name)
        train_val_stop_flag = int(current_data_length * train_val_scale)

        train_val_num = 0
        test_num = 0
        for i in current_data_index_list:
            src_img_path = os.path.join(current_class_data_path, current_all_data[i])
            if current_data_index_list.index(i) < train_val_stop_flag:
                shutil.copy2(src_img_path, train_val_folder)
                train_val_num += 1
            else:
                shutil.copy2(src_img_path, test_folder)
                test_num += 1

        print("*********************************{}*************************************".format(class_name))
        print("{}类按照{}：{}的比例划分完成，一共{}张图片".format(class_name, train_val_scale, test_scale, current_data_length))
        print("训练验证集{}：{}张".format(train_val_folder, train_val_num))
        print("测试集{}：{}张".format(test_folder, test_num))

if __name__ == '__main__':
    src_data_folder = "flower_photos"
    target_data_folder = "flower_photos_split1"
    data_set_split(src_data_folder, target_data_folder)
