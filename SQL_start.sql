DROP DATABASE IF EXISTS trademind_dev;

CREATE DATABASE trademind_dev;

USE trademind_dev;

CREATE TABLE Users (
    User_ID INT AUTO_INCREMENT PRIMARY KEY,
    User VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Hashed_Password VARCHAR(255) NOT NULL,
    Profile_Picture_Path VARCHAR(255) DEFAULT NULL
);

CREATE TABLE Tags (
    TagID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) UNIQUE NOT NULL
);

INSERT INTO Tags (Name) VALUES ('Finance'), ('Technology'), ('Services');


CREATE TABLE Models (
    Model_ID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Description TEXT,
    Name VARCHAR(255) NOT NULL,
    Like_Count INT DEFAULT 0,
    Subscribe_Count INT DEFAULT 0,
    Model_File_Path VARCHAR(255),  -- Store the file path instead of the blob
    FOREIGN KEY (UserID) REFERENCES Users(User_ID) ON DELETE CASCADE
);

CREATE TABLE Model_Tags (
    Model_ID INT,
    TagID INT,
    PRIMARY KEY (Model_ID, TagID),
    FOREIGN KEY (Model_ID) REFERENCES Models(Model_ID) ON DELETE CASCADE,
    FOREIGN KEY (TagID) REFERENCES Tags(TagID) ON DELETE CASCADE
);

CREATE TABLE User_Model_Subscribe (
    Model_ID INT,
    User_ID INT,
    PRIMARY KEY (Model_ID, User_ID),
    FOREIGN KEY (Model_ID) REFERENCES Models(Model_ID) ON DELETE CASCADE,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID) ON DELETE CASCADE
);

CREATE TABLE Reviews (
    Review_ID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Model_ID INT NOT NULL,
    Comment TEXT,
    Upvote INT DEFAULT 1,
    FOREIGN KEY (UserID) REFERENCES Users(User_ID) ON DELETE CASCADE,
    FOREIGN KEY (Model_ID) REFERENCES Models(Model_ID) ON DELETE CASCADE
);

CREATE TABLE Review_Upvotes (
    Review_ID INT NOT NULL,
    User_ID INT NOT NULL,
    PRIMARY KEY (Review_ID, User_ID),
    FOREIGN KEY (Review_ID) REFERENCES Reviews(Review_ID) ON DELETE CASCADE,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID) ON DELETE CASCADE
);

CREATE TABLE Likes (
    Like_ID INT AUTO_INCREMENT PRIMARY KEY,
    Model_ID INT NOT NULL,
    User_ID INT NOT NULL,
    FOREIGN KEY (Model_ID) REFERENCES Models(Model_ID) ON DELETE CASCADE,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID) ON DELETE CASCADE,
    UNIQUE (Model_ID, User_ID)  -- Ensure each user can like a model only once
);

CREATE TABLE Stocks (
    Stock_ID INT AUTO_INCREMENT PRIMARY KEY,
    Ticker VARCHAR(10) NOT NULL UNIQUE
);



CREATE TABLE MSE_Results (
    Result_ID INT AUTO_INCREMENT PRIMARY KEY,
    Stock_ID INT,
    Timeframe_Name VARCHAR(50),
    Model_ID INT,
    MSE_Value FLOAT,
    Evaluation_Date DATE,
    Raw_Data JSON,
    FOREIGN KEY (Stock_ID) REFERENCES Stocks(Stock_ID) ON DELETE CASCADE,
    FOREIGN KEY (Model_ID) REFERENCES Models(Model_ID) ON DELETE CASCADE
);

CREATE TABLE trademinds_nasdaqdata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE UNIQUE,
    open DECIMAL(10, 2),
    high DECIMAL(10, 2),
    low DECIMAL(10, 2),
    close DECIMAL(10, 2),
    volume BIGINT
);