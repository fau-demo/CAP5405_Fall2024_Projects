% Define paths
datasetFolder = 'Dataset/dataset'; % Path to your dataset
trainFolder = fullfile(datasetFolder, 'train'); % Path to train folder

% Verify if the train folder exists
if isfolder(trainFolder)
    disp('Train folder exists.');
else
    error('Train folder does not exist. Check the folder path.');
end

% List all files in the train folder
disp('Listing files in train folder:');
fileList = dir(fullfile(trainFolder, '*.*')); % List all files in the folder
disp({fileList.name}); % Display the names of the files in the folder

% Attempt to load images
imageFiles = dir(fullfile(trainFolder, '*.jpg')); % Change '*.jpg' to '*.png' or '*.*' as needed
if isempty(imageFiles)
    disp('No images found in the train folder. Check file extensions or folder structure.');
else
    % Load images into a cell array
    numImages = length(imageFiles);
    trainImages = cell(numImages, 1);

    for i = 1:numImages
        trainImages{i} = imread(fullfile(trainFolder, imageFiles(i).name));
    end

    % Display the number of images loaded
    disp(['Loaded ', num2str(numImages), ' training images.']);

    % Display the first image as a sample
    figure;
    imshow(trainImages{1});
    title('Sample Training Image');
end

% Debugging - Check train folder contents again
disp('Debugging: Contents of the train folder:');
debugFileList = dir(trainFolder);
disp({debugFileList.name}); % Display all file names in train folder

% Check if files in subfolders need to be considered
subfolderImageFiles = dir(fullfile(trainFolder, '**', '*.jpg')); % Recursive for .jpg files
if ~isempty(subfolderImageFiles)
    disp('Images found in subfolders:');
    disp({subfolderImageFiles.name});
else
    disp('No images found in subfolders.');
end