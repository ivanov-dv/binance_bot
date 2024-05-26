from dataclasses import dataclass, field


@dataclass
class StatusMonitoringOpenOrders:
    name: str
    amount_open_positions: int = 0
    open_orders_info: dict = field(default_factory=dict)


@dataclass
class StatusMonitoringPairs:
    name: str
    amount_pairs: int = 0
    master_iteration_count: int = 1
    slave_iteration_count: int = 1
    target_percent: int = 0
