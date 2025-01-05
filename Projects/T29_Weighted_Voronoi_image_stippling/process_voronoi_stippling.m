function process_voronoi_stippling(datasetPath, num_points)
    % Process all images in the dataset folder (including subfolders)
    % datasetPath: Path to the dataset folder
    % num_points: Number of stippling points per image

    % Check if the dataset path is valid
    if ~isfolder(datasetPath)
        error('The specified dataset path is not a valid folder.');
    end

    % Get all image files (.jpg, .jpeg, .png) recursively
    imageFiles = dir(fullfile(datasetPath, '**', '*.*')); % Include subfolders
    validExtensions = {'.jpg', '.jpeg', '.png'}; % Valid image extensions
    imageFiles = imageFiles(arrayfun(@(x) ismember(lower(fileparts(x.name)), validExtensions), imageFiles));

    if isempty(imageFiles)
        error('No valid images found in the specified dataset folder or its subfolders.');
    end

    % Create an output folder for processed images
    outputFolder = fullfile(datasetPath, 'Output');
    if ~exist(outputFolder, 'dir')
        mkdir(outputFolder); % Create the output folder if it doesn't exist
    end

    % Process each image
    for i = 1:length(imageFiles)
        % Full path to the current image
        imagePath = fullfile(imageFiles(i).folder, imageFiles(i).name);
        fprintf('Processing image: %s\n', imageFiles(i).name);

        % Apply the weighted Voronoi stippling algorithm
        stippled_img = weighted_voronoi_stippling(imagePath, num_points);

        % Save the stippled image
        [~, imageName, ~] = fileparts(imageFiles(i).name);
        outputFilePath = fullfile(outputFolder, [imageName, '_stippled.png']);
        imwrite(uint8(stippled_img), outputFilePath);
        fprintf('Stippled image saved to: %s\n', outputFilePath);
    end

    fprintf('Processing complete. Stippled images saved in: %s\n', outputFolder);
end

function stippled_img = weighted_voronoi_stippling(image_path, num_points)
    % Weighted Voronoi stippling for a single image
    % image_path: Path to the input image
    % num_points: Number of points for stippling

    % Load the image
    img = imread(image_path);
    if size(img, 3) == 3
        img_gray = rgb2gray(img); % Convert RGB to grayscale
    else
        img_gray = img; % Already grayscale
    end
    img_normalized = double(img_gray) / 255; % Normalize intensities to [0, 1]

    % Generate weighted random points
    points = generate_weighted_points(img_normalized, num_points);

    % Compute Voronoi diagram
    [vx, vy] = voronoi(points(:, 1), points(:, 2));
    figure;
    imshow(img_gray, []);
    hold on;
    plot(vx, vy, 'r-', 'LineWidth', 0.5);
    title('Voronoi Diagram');
    hold off;

    % Create stippled image
    stippled_img = ones(size(img_gray)) * 255; % Initialize canvas
    for i = 1:num_points
        x = round(points(i, 1));
        y = round(points(i, 2));
        x = max(min(x, size(img_gray, 2)), 1); % Ensure x is within bounds
        y = max(min(y, size(img_gray, 1)), 1); % Ensure y is within bounds
        stippled_img(y, x) = img_gray(y, x); % Assign intensity
    end

    % Display histogram and RGB visualization
    figure;
    histogram(img_gray, 256, 'FaceColor', 'b');
    title('Grayscale Histogram');

    stippled_rgb = ind2rgb(img_gray, gray(256)); % Convert grayscale to RGB
    for i = 1:num_points
        x = round(points(i, 1));
        y = round(points(i, 2));
        stippled_rgb(y, x, :) = [1, 0, 0]; % Highlight stippled points in red
    end
    figure;
    imshow(stippled_rgb);
    title('RGB Visualization with Stippled Points');
end

function points = generate_weighted_points(img, num_points)
    % Generate random points weighted by intensity
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
