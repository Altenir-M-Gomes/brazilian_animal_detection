# 🐾 Brazilian Animals Detection

This project was developed as part of my undergraduate thesis (TCC). The main goal was to detect animals in images using neural networks and identify the species present.

To achieve this, I used publicly available image datasets such as [LILA BC](https://lila.science/datasets/wcscameratraps) and [Camera Trap Surveys](https://figshare.com/articles/dataset/Files_from_data_paper_Camera_trap_surveys_of_Atlantic_Forest_mammals_a_dataset_for_analyses_considering_imperfect_detection_2004-2020_/23549451/1).

The project is organized into folders, each with a specific purpose. For example:
- `/model_select`: contains model comparison experiments. Here, I tested different architectures to understand which one performed best for my problem.
- `/animal_detection`: includes the implementation of the selected neural network model. The first step is to detect whether an image contains an animal or not.
- `/loands_images`: for download the images to my local machine.
