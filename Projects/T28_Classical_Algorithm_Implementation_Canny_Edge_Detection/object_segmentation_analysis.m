function object_segmentation_analysis()
    % Dataset path
    folder = '/MATLAB Drive/SUJANADIP/natural_images';
    output_image_path = '/MATLAB Drive/SUJANADIP/object_segmentation_results.png';
    output_pdf_path = '/MATLAB Drive/SUJANADIP/object_segmentation_report.pdf';
    num_images = 5; % Number of images to showcase

    % Ensure the folder exists
    if ~isfolder(folder)
        error('The specified folder does not exist: %s', folder);
    end

    % Get all image files recursively
    files = get_all_images_recursive(folder);

    % Check if valid images exist
    if isempty(files)
        error('No image files found in the folder or subfolders: %s', folder);
    end

    % Showcase results for segmentation
    fprintf('\nShowcasing Object Segmentation Results with Metrics:\n');
    showcase_segmentation_with_metrics(files, num_images, output_image_path);

    % Save segmentation results as a PDF
    fprintf('\nSaving Segmentation Results as a PDF Report:\n');
    save_segmentation_results_as_pdf(files, output_pdf_path, num_images);

    fprintf('\nResults saved to:\nPDF: %s\nImage: %s\n', output_pdf_path, output_image_path);
end

function files = get_all_images_recursive(folder)
    % Recursively get all image files from folder and subfolders
    file_types = {'*.png', '*.jpg', '*.jpeg', '*.bmp'};
    files = [];
    for i = 1:length(file_types)
        files = [files; dir(fullfile(folder, '**', file_types{i}))];
    end
end

function [segmented_image, num_objects, object_sizes] = segment_objects(image_path)
    % Read the image
    image = imread(image_path);
    gray_image = rgb2gray(image);

    % Canny Edge Detection
    edges = edge(gray_image, 'Canny');

    % Find Connected Components
    connected_components = bwconncomp(edges);

    % Metrics: Number of Objects and Sizes
    num_objects = connected_components.NumObjects;
    object_sizes = cellfun(@numel, connected_components.PixelIdxList);
    object_sizes = object_sizes(object_sizes > 50); % Filter small objects

    % Draw Contours
    segmented_image = image;
    for i = 1:num_objects
        if numel(connected_components.PixelIdxList{i}) > 50
            [y, x] = ind2sub(size(edges), connected_components.PixelIdxList{i});
            segmented_image = insertShape(segmented_image, 'Rectangle', ...
                [min(x), min(y), max(x)-min(x)+1, max(y)-min(y)+1], 'Color', 'green');
        end
    end
end

function showcase_segmentation_with_metrics(files, num_images, output_image_path)
    fprintf('%-40s %-15s %-20s\n', 'Image Name', 'Number of Objects', 'Average Object Size');
    fprintf('%s\n', repmat('-', 1, 80));

    num_files = min(num_images, length(files));
    rows = num_files; % Number of rows for the output image
    figure;

    for idx = 1:num_files
        filename = files(idx).name;
        image_path = fullfile(files(idx).folder, filename);

        % Segment Objects
        [segmented_image, num_objects, object_sizes] = segment_objects(image_path);

        % Calculate Metrics
        avg_object_size = mean(object_sizes);
        fprintf('%-40s %-15d %-20.2f\n', filename, num_objects, avg_object_size);

        % Plot Original and Segmented Images
        original_image = imread(image_path);

        subplot(rows, 2, 2 * (idx - 1) + 1);
        imshow(original_image);
        title(['Original: ', filename], 'Interpreter', 'none');

        subplot(rows, 2, 2 * (idx - 1) + 2);
        imshow(segmented_image);
        title(['Segmented: ', filename, ' (', num2str(num_objects), ' Objects)'], 'Interpreter', 'none');
    end

    % Save results as an image
    saveas(gcf, output_image_path);
    close(gcf);
end

function save_segmentation_results_as_pdf(files, pdf_path, num_images)
    % Initialize PDF
    import mlreportgen.dom.*;
    doc = Document(pdf_path, 'pdf');

    num_files = min(num_images, length(files));

    for idx = 1:num_files
        filename = files(idx).name;
        image_path = fullfile(files(idx).folder, filename);

        % Segment Objects
        [segmented_image, num_objects, object_sizes] = segment_objects(image_path);

        % Create Figures
        original_image = imread(image_path);

        figure;
        subplot(1, 2, 1);
        imshow(original_image);
        title(['Original: ', filename], 'Interpreter', 'none');

        subplot(1, 2, 2);
        imshow(segmented_image);
        title(['Segmented: ', filename, ' (', num2str(num_objects), ' Objects)'], 'Interpreter', 'none');

        % Save temporary image for PDF
        temp_image_path = fullfile(tempdir, ['temp_', num2str(idx), '.png']);
        saveas(gcf, temp_image_path);

        % Add image to PDF
        img = Image(temp_image_path);
        append(doc, img);

        % Close figure
        close(gcf);
    end

    close(doc);
end
