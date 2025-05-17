from scipy.stats import truncnorm

def truncated_normal_distribution(center_time, std_minutes=3):
    a, b = -30 / std_minutes, 30 / std_minutes  # Standardized bounds
    return truncnorm.rvs(a, b, loc=center_time, scale=std_minutes)