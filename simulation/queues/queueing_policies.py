from shared_queue_policy import SharedQueuePolicy
from seperate_queues_policy import SeparateQueuesPolicy

class QueueingPolicyRegistry:
    """
    Registry for queueing policies.
    
    Example usage:
        # Get the registry instance
        registry = QueueingPolicyRegistry()
        
        # Get a specific policy class
        policy_class = registry.get_policy('policy_name')
        
        # Create an instance of the policy
        policy_instance = policy_class()
    """
    def __init__(self):
        self._policies = {
            'shared_queue': SharedQueuePolicy,
            'separate_queues': SeparateQueuesPolicy
        }
    
    def get_policy(self, policy_name: str):
        """
        Get a queueing policy class by its name.
        
        Args:
            policy_name (str): The name of the policy to retrieve
            
        Returns:
            The queueing policy class
            
        Raises:
            KeyError: If the policy name is not found in the registry
        """
        if policy_name not in self._policies:
            raise KeyError(f"Queueing policy '{policy_name}' not found. Available policies: {list(self._policies.keys())}")
        return self._policies[policy_name]
    
    def list_available_policies(self):
        """
        Returns a list of all available policy names.
        """
        return list(self._policies.keys())

# Create a singleton instance
queueing_policies = QueueingPolicyRegistry()