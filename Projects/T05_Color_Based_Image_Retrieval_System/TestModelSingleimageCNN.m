% Set dataset path
datasetPath = fullfile(pwd, 'Dataset'); % Adjust the folder name if necessary

% Check if the dataset folder exists
if ~isfolder(datasetPath)
    error('Dataset folder not found. Make sure it is correctly uploaded.');
end

% Load the dataset
imds = imageDatastore(datasetPath, ...
    'IncludeSubfolders', true, ...
    'LabelSource', 'foldernames');

% Split data into training and validation sets
[trainImgs, valImgs] = splitEachLabel(imds, 0.8, 'randomized');

% Resize the images to 224x224 for compatibility (augmentation)
augmentedTrainImgs = augmentedImageDatastore([224 224], trainImgs);
augmentedValImgs = augmentedImageDatastore([224 224], valImgs);

% Define CNN model
layers = [
    imageInputLayer([224 224 3], 'Name', 'input')
    convolution2dLayer(3, 16, 'Padding', 'same', 'Name', 'conv1')
    batchNormalizationLayer('Name', 'batchnorm1')
    reluLayer('Name', 'relu1')
    maxPooling2dLayer(2, 'Stride', 2, 'Name', 'maxpool1')
    fullyConnectedLayer(numel(unique(imds.Labels)), 'Name', 'fc')
    softmaxLayer('Name', 'softmax')
    classificationLayer('Name', 'output')
];

% Training options
options = trainingOptions('adam', ...
    'InitialLearnRate', 0.001, ...
    'MaxEpochs', 5, ...
    'MiniBatchSize', 32, ...
    'Shuffle', 'every-epoch', ...
    'ValidationData', augmentedValImgs, ...
    'ValidationFrequency', 30, ...
    'Verbose', true, ...
    'Plots', 'training-progress');

% Train the model
net = trainNetwork(augmentedTrainImgs, layers, options);

% Functionality to upload and test an image
disp('Select an image to upload and test:');
[filename, pathname] = uigetfile({'*.jpg;*.png;*.jpeg;*.tiff', 'Image Files (*.jpg, *.png, *.jpeg, *.tiff)'}, 'Select an Image');
if isequal(filename, 0)
    disp('No file selected.');
else
    queryImgPath = fullfile(pathname, filename);
    queryImg = imread(queryImgPath); % Read the uploaded image
    resizedQueryImg = imresize(queryImg, [224 224]); % Resize to match input layer dimensions
    predictedLabel = classify(net, resizedQueryImg); % Classify the image
    
    % Display the test image and predicted label
    figure;
    imshow(resizedQueryImg);
    title(['Predicted Label: ', char(predictedLabel)]);
    disp(['The predicted label for the uploaded image is: ', char(predictedLabel)]);
end
