CREATE TABLE `tbl_without_index` (
    `id` BIGINT UNSIGNED NOT NULL,
    `done` BOOLEAN NOT NULL DEFAULT FALSE,
    
    PRIMARY KEY (`id`)
);

CREATE TABLE `tbl_with_index` LIKE `tbl_without_index`;

CREATE INDEX `done_and_id` ON `tbl_with_index` (`done`, `id`);
