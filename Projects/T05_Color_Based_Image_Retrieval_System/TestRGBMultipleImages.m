% Set dataset path
datasetPath = fullfile(pwd, 'Dataset'); % Adjust folder name as needed

% Check if the dataset folder exists
if ~isfolder(datasetPath)
    error('Dataset folder not found. Make sure it is correctly uploaded.');
end

% Load all images from the dataset
imageFiles = dir(fullfile(datasetPath, '**', '*.jpg')); % Adjust for other formats if needed
numImages = length(imageFiles);

% Prompt user to select color space
disp('Select the color space for histogram calculation:');
disp('1: RGB');
disp('2: HSV');
disp('3: LAB');
colorSpaceChoice = input('Enter your choice (1/2/3): ');

% Initialize storage for histograms
histograms = zeros(numImages, 256 * 3); % 256 bins per channel, 3 channels

% Function to convert image based on color space
function convertedImg = convertColorSpace(img, space)
    switch space
        case 1
            convertedImg = img; % RGB
        case 2
            convertedImg = rgb2hsv(img); % HSV
        case 3
            convertedImg = rgb2lab(img); % LAB
        otherwise
            error('Invalid color space choice');
    end
end

% Calculate histograms for each image
disp('Processing images and calculating histograms...');
for i = 1:numImages
    imgPath = fullfile(imageFiles(i).folder, imageFiles(i).name);
    img = imread(imgPath);
    img = imresize(img, [224 224]); % Resize for consistency
    img = convertColorSpace(img, colorSpaceChoice); % Convert to selected color space
    
    % Calculate histograms for each channel
    rHist = imhist(img(:, :, 1), 256);
    gHist = imhist(img(:, :, 2), 256);
    bHist = imhist(img(:, :, 3), 256);
    
    % Normalize histograms
    rHist = rHist / sum(rHist);
    gHist = gHist / sum(gHist);
    bHist = bHist / sum(bHist);
    
    % Concatenate histograms
    histograms(i, :) = [rHist; gHist; bHist]';
    
    if mod(i, 100) == 0
        fprintf('Processed %d/%d images\n', i, numImages);
    end
end
disp('Histogram calculation completed.');

% Functionality to upload and test a query image
disp('Select a query image to upload and test:');
[filename, pathname] = uigetfile({'*.jpg;*.png;*.jpeg;*.tiff', 'Image Files (*.jpg, *.png, *.jpeg, *.tiff)'}, 'Select an Image');
if isequal(filename, 0)
    disp('No file selected.');
else
    queryImgPath = fullfile(pathname, filename);
    queryImg = imread(queryImgPath);
    queryImg = imresize(queryImg, [224 224]); % Resize to match dataset images
    queryImg = convertColorSpace(queryImg, colorSpaceChoice); % Convert to selected color space
    
    % Calculate histogram for the query image
    rHistQuery = imhist(queryImg(:, :, 1), 256);
    gHistQuery = imhist(queryImg(:, :, 2), 256);
    bHistQuery = imhist(queryImg(:, :, 3), 256);
    
    % Normalize query histograms
    rHistQuery = rHistQuery / sum(rHistQuery);
    gHistQuery = gHistQuery / sum(gHistQuery);
    bHistQuery = bHistQuery / sum(bHistQuery);
    
    queryHistogram = [rHistQuery; gHistQuery; bHistQuery]';
    
    % Compare query histogram with dataset histograms using Euclidean distance
    distances = zeros(numImages, 1);
    for i = 1:numImages
        distances(i) = norm(histograms(i, :) - queryHistogram);
    end
    
    % Sort distances to find top matches
    [~, sortedIndices] = sort(distances);
    topN = 5; % Number of top matches to display
    topMatches = sortedIndices(1:topN);
    
    % Display query image and top matches
    figure;
    subplot(2, 3, 1);
    imshow(queryImg);
    title('Query Image');
    
    for i = 1:topN
        matchImgPath = fullfile(imageFiles(topMatches(i)).folder, imageFiles(topMatches(i)).name);
        matchImg = imread(matchImgPath);
        subplot(2, 3, i + 1);
        imshow(matchImg);
        title(sprintf('Match %d (Score: %.2f)', i, distances(topMatches(i))));
    end
    
    % Validation Phase: Calculate precision, recall, and F1-Score
    disp('Validation Phase: Calculating Precision, Recall, and F1-Score...');
    % Example validation: Add a label file 'imageLabels.mat'
    load('imageLabels.mat'); % Contains 'queryCategory' and 'datasetCategories'
    
    % Retrieve categories for matches
    queryCategory = imageLabels.queryCategory; % Query image's category
    retrievedCategories = imageLabels.datasetCategories; % Dataset categories
    
    precisionScores = zeros(topN, 1);
    recallScores = zeros(topN, 1);
    
    for i = 1:topN
        matchCategory = retrievedCategories(topMatches(i));
        isRelevant = strcmp(queryCategory, matchCategory);
        precisionScores(i) = sum(isRelevant) / i; % Precision
        recallScores(i) = sum(isRelevant) / numel(find(strcmp(datasetCategories, queryCategory))); % Recall
    end
    
    f1Scores = 2 * (precisionScores .* recallScores) ./ (precisionScores + recallScores);
    
    % Display validation metrics
    disp('Validation Metrics:');
    for i = 1:topN
        fprintf('Match %d: Precision=%.2f, Recall=%.2f, F1-Score=%.2f\n', ...
            i, precisionScores(i), recallScores(i), f1Scores(i));
    end
    
    % Plot validation metrics
    figure;
    subplot(1, 3, 1);
    plot(1:topN, precisionScores, '-o');
    title('Precision');
    xlabel('Top-N Matches');
    ylabel('Precision');
    
    subplot(1, 3, 2);
    plot(1:topN, recallScores, '-o');
    title('Recall');
    xlabel('Top-N Matches');
    ylabel('Recall');
    
    subplot(1, 3, 3);
    plot(1:topN, f1Scores, '-o');
    title('F1-Scores');
    xlabel('Top-N Matches');
    ylabel('F1-Score');
end
