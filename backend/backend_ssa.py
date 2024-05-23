from lcls_tools.superconducting.sc_linac import SSA


class BackendSSA(SSA):
    def __init__(self, cavity):
        super().__init__(cavity)
        self.alarm_sevr_pv: str = self.pv_addr("AlarmSummary.SEVR")
