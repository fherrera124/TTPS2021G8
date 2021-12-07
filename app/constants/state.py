class StudyState:
    """
    Constants for the various states of a study
    """

    STATE_ONE = "Esperando comprobante de pago"
    STATE_ONE_ERROR = "Anulado por falta de pago"
    STATE_TWO = "Esperando consentimiento firmado"
    STATE_THREE = "Esperando selección de turno"
    STATE_FOUR = "Esperando toma de muestra"
    STATE_FIVE = "Esperando retiro de muestra"
    STATE_SIX = "Esperando lote de muestra"
    STATE_SEVEN = "Esperando resultado biotecnológico"
    STATE_EIGHT = "Esperando interpretación de resultados e informes"
    STATE_NINE = "Esperando ser entregado a médico derivante"
    STATE_ENDED = "Resultado entregado"


class SampleBatchState:

    STATE_ONE = "En procesamiento"
    STATE_TWO = "Procesado"