Client provides email and password, which is sent to the server
Server then verifies that email and password are correct and responds with an auth token
Client stores the token and sends it along with all subsequent requests to the API
Server decodes the token and validates it

###################---SQL query to get model and associated user data---##################

SELECT 
    m.Model_ID,
    m.Name AS Model_Name,
    m.Description AS Model_Description,
    m.Like_Count,
    m.Subscribe_Count,
    m.Model_File_Path,
    u.User_ID,
    u.User AS User_Name,
    u.Profile_Picture_Path AS User_Profile_Picture
FROM 
    Models m
JOIN 
    Users u ON m.UserID = u.User_ID;

########---------------------_###############
SELECT ALL REVIEWID , COMMENT  , UPVOTES AND REVIEWER AND MODEL  
SELECT 
    r.Review_ID,
    r.Comment,
    r.Upvote,
    r.Model_ID,
    r.UserID AS Reviewer_ID,
    u.User AS Reviewer_Name,
    u.Profile_Picture_Path AS Reviewer_Profile_Picture
FROM 
    Reviews r
JOIN 
    Users u ON r.UserID = u.User_ID;


####Get all people who liked a id #####
SELECT 
    l.Like_ID,
    l.Model_ID,
    l.User_ID AS Liker_ID,
    u.User AS Liker_Name,
    u.Profile_Picture_Path AS Liker_Profile_Picture
FROM 
    Likes l
JOIN 
    Users u ON l.User_ID = u.User_ID;


###Get all subscriber_id_to a model
SELECT 
    s.Model_ID,
    s.User_ID AS Subscriber_ID,
    u.User AS Subscriber_Name,
    u.Profile_Picture_Path AS Subscriber_Profile_Picture
FROM 
    User_Model_Subscribe s
JOIN 
    Users u ON s.User_ID = u.User_ID;