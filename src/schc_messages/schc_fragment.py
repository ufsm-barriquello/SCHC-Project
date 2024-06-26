"""schc_fragment: SCHCFragment Class"""

from schc_messages import SCHCMessage


class SCHCFragment(SCHCMessage):
    """
    SCHC Fragment Abstract Class

    |-- SCHC Fragment Header -|
    +--------+------+---+-----+------------------+--------------------+
    | RuleID | Dtag | W | ··· | Fragment Payload | padding (as needed)|
    +--------+------+---+-----+------------------+--------------------+
    """

    def __init__(self, rule_id, protocol=1, dtag=None, w=None, fcn=None, rcs=None):
        """
        Constructor

        Parameters
        ----------
        rule_id
        protocol :
            Optional
        dtag :
            Optional
        w :
            Optional
        fcn :
            Optional
        rcs :
            Optional

        See Also
        --------
        schc_message.schc_header.schc_header.SCHCHeader :
            Description of Other Parameters
        """
        super().__init__(rule_id=rule_id, protocol=protocol, dtag=dtag,
                         w=w, fcn=fcn, rcs=rcs)

    def add_tile(self, tile):
        """
        Adds tile to payload of message

        Parameters
        ----------
        tile : Tile
            A tile to add to payload

        Returns
        -------
        int :
            Size of current SCHC Fragment
        """
        payload_size = self.payload.add_content(tile.as_bits())
        self.size = self.header.size + payload_size + self.padding.size
        return self.size

    def as_bits(self):
        """
        Bits sequence representation

        Returns
        -------
        str :
            Bits sequence in a string
        """
        return self.header.as_bits() + self.payload.as_bits() + self.padding.as_bits()

    def as_text(self):
        """
        Writes message with specifications

        Returns
        -------
        str :
            SCHC Message as text format
        """
        header_text = "|--- SCHC Fragment Header {}---|\n"
        return self.base_as_text(header_text)
