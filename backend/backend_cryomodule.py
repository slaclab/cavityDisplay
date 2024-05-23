from lcls_tools.superconducting.sc_linac import Cryomodule


class BackendCryomodule(Cryomodule):
    def __init__(
        self,
        cryo_name,
        linac_object,
    ):
        super().__init__(
            cryo_name=cryo_name,
            linac_object=linac_object,
        )

    @property
    def pydm_macros(self):
        """
        Currenlty only used for NIRP fault, but I think we can just keep adding
        to this list
        :return:
        """
        return "AREA={linac_name},CM={cm_name},RFNAME=CM{cm_name}".format(
            linac_name=self.linac.name, cm_name=self.name
        )
