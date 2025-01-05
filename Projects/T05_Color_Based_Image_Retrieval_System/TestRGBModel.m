% Set dataset path
datasetPath = fullfile(pwd, 'Dataset'); % Adjust folder name as needed

% Check if the dataset folder exists
if ~isfolder(datasetPath)
    error('Dataset folder not found. Make sure it is correctly uploaded.');
end

% Load all images from the dataset
imageFiles = dir(fullfile(datasetPath, '**', '*.jpg')); % Adjust for other formats if needed
numImages = length(imageFiles);

% Initialize storage for histograms
histograms = zeros(numImages, 256 * 3); % 256 bins per channel, 3 channels

% Initialize storage for average RGB values
averageRGBValues = zeros(numImages, 3);

% Calculate histograms and average RGB values for each image
disp('Processing images and calculating histograms...');
for i = 1:numImages
    imgPath = fullfile(imageFiles(i).folder, imageFiles(i).name);
    img = imread(imgPath);
    img = imresize(img, [224 224]); % Resize for consistency
    
    % Calculate histograms for each RGB channel
    rHist = imhist(img(:, :, 1), 256);
    gHist = imhist(img(:, :, 2), 256);
    bHist = imhist(img(:, :, 3), 256);
    
    % Normalize histograms (optional but improves accuracy)
    rHist = rHist / sum(rHist);
    gHist = gHist / sum(gHist);
    bHist = bHist / sum(bHist);
    
    % Store histograms
    histograms(i, :) = [rHist; gHist; bHist]';
    
    % Calculate average RGB values
    averageRGBValues(i, :) = mean(reshape(img, [], 3));
    
    if mod(i, 100) == 0
        fprintf('Processed %d/%d images\n', i, numImages);
    end
end
disp('Histogram calculation and RGB value extraction completed.');

% Functionality to upload and test a query image
disp('Select a query image to upload and test:');
[filename, pathname] = uigetfile({'*.jpg;*.png;*.jpeg;*.tiff', 'Image Files (*.jpg, *.png, *.jpeg, *.tiff)'}, 'Select an Image');
if isequal(filename, 0)
    disp('No file selected.');
else
    queryImgPath = fullfile(pathname, filename);
    queryImg = imread(queryImgPath);
    queryImg = imresize(queryImg, [224 224]); % Resize to match dataset images
    
    % Calculate histogram for the query image
    rHistQuery = imhist(queryImg(:, :, 1), 256);
    gHistQuery = imhist(queryImg(:, :, 2), 256);
    bHistQuery = imhist(queryImg(:, :, 3), 256);
    
    % Normalize query histograms
    rHistQuery = rHistQuery / sum(rHistQuery);
    gHistQuery = gHistQuery / sum(gHistQuery);
    bHistQuery = bHistQuery / sum(bHistQuery);
    
    queryHistogram = [rHistQuery; gHistQuery; bHistQuery]';
    
    % Calculate average RGB values for the query image
    queryAvgRGB = mean(reshape(queryImg, [], 3));
    
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
    title(sprintf('Query Image\nRGB: [%d, %d, %d]', round(queryAvgRGB)));
    
    for i = 1:topN
        matchImgPath = fullfile(imageFiles(topMatches(i)).folder, imageFiles(topMatches(i)).name);
        matchImg = imread(matchImgPath);
        matchAvgRGB = averageRGBValues(topMatches(i), :);
        
        subplot(2, 3, i + 1);
        imshow(matchImg);
        title(sprintf('Match %d\nRGB: [%d, %d, %d]', i, round(matchAvgRGB)));
    end
    
    % Plot histograms of the query image and top matches
    figure;
    for i = 1:topN+1
        if i == 1
            img = queryImg;
            imgTitle = 'Query Image Histogram';
        else
            imgPath = fullfile(imageFiles(topMatches(i-1)).folder, imageFiles(topMatches(i-1)).name);
            img = imread(imgPath);
            imgTitle = sprintf('Match %d Histogram', i-1);
        end
        
        rHist = imhist(img(:, :, 1), 256) / numel(img(:, :, 1));
        gHist = imhist(img(:, :, 2), 256) / numel(img(:, :, 2));
        bHist = imhist(img(:, :, 3), 256) / numel(img(:, :, 3));
        
        subplot(2, 3, i);
        hold on;
        bar(rHist, 'r');
        bar(gHist, 'g');
        bar(bHist, 'b');
        hold off;
        title(imgTitle);
        xlim([0 256]);
    end
end
