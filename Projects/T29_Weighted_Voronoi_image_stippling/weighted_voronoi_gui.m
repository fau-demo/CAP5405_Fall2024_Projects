function weighted_voronoi_gui
    % GUI for Weighted Voronoi Image Stippling

    % Create the main figure
    hFig = figure('Name', 'Weighted Voronoi Stippling', 'NumberTitle', 'off', ...
        'Position', [300, 200, 700, 500], 'Resize', 'off', 'MenuBar', 'none');
    
    % Dataset Folder Selection
    uicontrol('Style', 'text', 'Position', [30, 430, 120, 30], ...
        'String', 'Dataset Folder:', 'HorizontalAlignment', 'right');
    hDatasetPath = uicontrol('Style', 'edit', 'Position', [160, 435, 320, 25], ...
        'HorizontalAlignment', 'left', 'Enable', 'inactive');
    uicontrol('Style', 'pushbutton', 'Position', [500, 435, 60, 25], ...
        'String', 'Browse', 'Callback', @(~, ~) selectFolder(hDatasetPath));
    
    % Number of Points
    uicontrol('Style', 'text', 'Position', [30, 390, 120, 30], ...
        'String', 'Number of Points:', 'HorizontalAlignment', 'right');
    hNumPoints = uicontrol('Style', 'edit', 'Position', [160, 395, 80, 25], ...
        'String', '100', 'HorizontalAlignment', 'left');
    
    % Run Button
    uicontrol('Style', 'pushbutton', 'Position', [260, 360, 120, 40], ...
        'String', 'Run Stippling', 'FontSize', 12, ...
        'Callback', @(~, ~) runStippling(hDatasetPath, hNumPoints));
    
    % Image Navigation Buttons
    hPrevBtn = uicontrol('Style', 'pushbutton', 'Position', [200, 50, 80, 40], ...
        'String', 'Previous', 'Enable', 'off', 'Callback', @(~, ~) showImage(-1));
    hNextBtn = uicontrol('Style', 'pushbutton', 'Position', [300, 50, 80, 40], ...
        'String', 'Next', 'Enable', 'off', 'Callback', @(~, ~) showImage(1));
    
    % Status Box
    hStatus = uicontrol('Style', 'text', 'Position', [30, 20, 640, 30], ...
        'String', 'Status: Ready', 'HorizontalAlignment', 'left', 'BackgroundColor', 'white');
    
    % Axes for Image Display
    hAxes = axes('Parent', hFig, 'Position', [0.15, 0.2, 0.7, 0.5]);
    axis off;
    
    % Data Storage
    images = [];
    currentIndex = 0;

    % Nested functions
    function selectFolder(hPathField)
        folder = uigetdir();
        if folder ~= 0
            hPathField.String = folder;
        end
    end

    function runStippling(hPathField, hNumPointsField)
        datasetPath = hPathField.String;
        numPoints = str2double(hNumPointsField.String);
        
        if isempty(datasetPath) || ~isfolder(datasetPath)
            hStatus.String = 'Status: Invalid dataset folder!';
            return;
        end
        if isnan(numPoints) || numPoints <= 0
            hStatus.String = 'Status: Invalid number of points!';
            return;
        end

        % Process Images
        try
            hStatus.String = 'Status: Processing images...';
            drawnow;
            [images, outputFolder] = process_voronoi_stippling(datasetPath, numPoints);
            currentIndex = 1;
            hPrevBtn.Enable = 'off';
            hNextBtn.Enable = 'on';
            showImage(0); % Show the first image
            hStatus.String = ['Status: Processing complete! Images saved in: ', outputFolder];
        catch ME
            hStatus.String = ['Status: Error - ', ME.message];
        end
    end

    function showImage(direction)
        if isempty(images)
            return;
        end
        currentIndex = currentIndex + direction;
        if currentIndex <= 1
            currentIndex = 1;
            hPrevBtn.Enable = 'off';
        else
            hPrevBtn.Enable = 'on';
        end
        if currentIndex >= length(images)
            currentIndex = length(images);
            hNextBtn.Enable = 'off';
        else
            hNextBtn.Enable = 'on';
        end
        % Display the current image
        axes(hAxes);
        imshow(images{currentIndex});
        title(sprintf('Processed Image %d/%d', currentIndex, length(images)));
    end
end

function [imageArray, outputFolder] = process_voronoi_stippling(datasetPath, num_points)
    imageFiles = dir(fullfile(datasetPath, '**', '*.jpg')); % Recursive search
    if isempty(imageFiles)
        error('No valid images found in the specified dataset folder or its subfolders.');
    end

    numImages = min(20, length(imageFiles)); % Limit to 20 images
    imageFiles = imageFiles(1:numImages);
    outputFolder = fullfile(datasetPath, 'Output');
    if ~exist(outputFolder, 'dir')
        mkdir(outputFolder);
    end

    imageArray = cell(1, numImages); % Store processed images
    for i = 1:numImages
        imagePath = fullfile(imageFiles(i).folder, imageFiles(i).name);
        stippled_img = weighted_voronoi_stippling(imagePath, num_points);
        [~, imageName, ~] = fileparts(imageFiles(i).name);
        outputFilePath = fullfile(outputFolder, [imageName, '_stippled.png']);
        imwrite(stippled_img, outputFilePath);
        imageArray{i} = stippled_img; % Store in array
    end
end

function stippled_img = weighted_voronoi_stippling(image_path, num_points)
    img = imread(image_path);
    if size(img, 3) == 1
        img = repmat(img, 1, 1, 3); % Convert grayscale to RGB
    end
    
    % Normalize intensity for stippling
    img_gray = rgb2gray(img);
    img_normalized = double(img_gray) / 255;

    % Generate weighted random points
    points = generate_weighted_points(img_normalized, num_points);

    % Create a blank canvas for the stippled image
    stippled_img = img; % Start with the original image

    % Compute Voronoi diagram
    [vx, vy] = voronoi(points(:, 1), points(:, 2));

    % Overlay the Voronoi lines and points on the image
    figure;
    imshow(stippled_img);
    hold on;
    plot(vx, vy, 'g-', 'LineWidth', 1); % Green lines for Voronoi
    scatter(points(:, 1), points(:, 2), 30, 'r', 'filled'); % Red points for stippling
    hold off;

    % Add stippled points to the image
    for i = 1:num_points
        x = round(points(i, 1));
        y = round(points(i, 2));
        x = max(min(x, size(img, 2)), 1); % Ensure x is within bounds
        y = max(min(y, size(img, 1)), 1); % Ensure y is within bounds
        stippled_img(y, x, :) = [255, 0, 0]; % Assign red color to points
    end
end

function points = generate_weighted_points(img, num_points)
    [h, w] = size(img);
    points = zeros(num_points, 2);
    for i = 1:num_points
        while true
            x = randi(w);
            y = randi(h);
            if rand() < img(y, x) % Higher probability for brighter pixels
                points(i, :) = [x, y];
                break;
            end
        end
    end
end
