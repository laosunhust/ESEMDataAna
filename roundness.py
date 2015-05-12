import mahotas.features.shape
import numpy as np
import mahotas as mh
from mahotas.features.shape import roundness, eccentricity
  
def test_eccentricity():
    D = mh.disk(32, 2)
    #print(D)
    ecc = mahotas.features.shape.eccentricity(D)
    assert 0 <= ecc < .01
  
    Index = np.indices((33,33)).astype(float)
    #print(Index)
    Index -= 15
    X,Y = Index
    ellipse = ((X**2+2*Y**2) < 12**2)
    assert 0 < mahotas.features.shape.eccentricity(ellipse) < 1
    
def test_roundness():
    Y,X = -240 + np.indices((480,480)).astype(float)

    #X[0][0] = X[0][0] - 1
    #print(X[0][0])
    #print((Y ** 2. + X**2.) <= 100**2.)
    r = roundness( (Y ** 2. + X**2.) <= 100**2.)
    print(r)
    #print(X)
    #print(Y)
    #print((Y ** 2. + X**2.) <= 150**2.)
    r = roundness( ((Y+1) ** 2. + X**2.) <= 100**2. )
    assert r > 0
    print(r)
    #r2 = roundness( (Y ** 2. + 2* X**2.) < 4**2. )
    #assert r2 > 0
    #print(r2)
    #r3 = roundness(X1,Y1)
    #print(r3)
    #assert r2 < r

test_roundness()
test_eccentricity()
