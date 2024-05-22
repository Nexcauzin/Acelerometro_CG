# Variáveis avulsas
dt = 0.1

Kalman1DOutput = [0,0] # Predição de angulo / Incerteza de predição

# Kalman 1d, conferir as incertezas depois para calibrar
def kalman_1d(KalmanState, KalmanUncertainty, KalmanInput, KalmanMeasurement):
    KalmanState = KalmanState + dt*KalmanInput
    KalmanUncertainty = KalmanUncertainty + dt*dt*4*4
    KalmanGain = KalmanUncertainty*1/(1*KalmanUncertainty + 3*3)
    KalmanState = KalmanState + KalmanGain*(KalmanMeasurement - KalmanState)
    KalmanUncertainty=(1-KalmanGain)*KalmanUncertainty
    Kalman1DOutput[0] = KalmanState
    Kalman1DOutput[1] = KalmanUncertainty
    return Kalman1DOutput
