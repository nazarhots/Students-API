from logger.logger import create_logger

logger = create_logger()


def validate_values(group_id, first_name, last_name):
    if not all([group_id, first_name, last_name]):
        logger.debug(
                f"Client sent bad args, group_id - {group_id}, first_name - {first_name}, last_name - {last_name}")
        return "Values can't be empty", 400
        
    if len(first_name) > 50:
        logger.debug(f"Client sent to long first name - {first_name}")
        return "First name should be less than 50", 400
    
    if len(last_name) > 50:
        logger.debug(f"Client sent to long last name - {last_name}")
        return "Last name should be less than 50", 400
