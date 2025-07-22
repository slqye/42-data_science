SELECT 
    day,
    AVG(avg_spend) AS avg_spend_per_user
FROM (
    SELECT 
        DATE(event_time) AS day,
        user_id,
        AVG(price) AS avg_spend
    FROM 
        customers
    WHERE 
        event_type = 'purchase'
    GROUP BY 
        day, user_id
) AS daily_user_avg
GROUP BY 
    day
ORDER BY 
    day;
