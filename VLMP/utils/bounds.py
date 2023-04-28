import logging

class BoundsBox:

    def __init__(self,nParticles,concentration):
        self.logger = logging.getLogger('VLMP')
        L = round((nParticles/concentration)**(1./3.),2)
        self.box = [L,L,L]

        self.logger.debug(f"[BoundsBox] Bounds box, box size : {L}")

    def getSimulationBox(self):
        return self.box

    def getSimulationBounds(self):
        return {}

    def check(self,position):

        boxX,boxY,boxZ = [b/2.0 for b in self.box]

        x,y,z = position
        if (x>boxX or y>boxY or z>boxZ or x<-boxX or y<-boxY or z<-boxZ):
            return False

        return True

class BoundsPlates:

    def __init__(self,nParticles,concentration,particleDiameter,padding,aspectRatio):
        self.logger = logging.getLogger('VLMP')

        self.particleDiameter = particleDiameter

        L = round((nParticles/(concentration*aspectRatio))**(1./3.),2)

        Lz = aspectRatio*L

        self.plateTop    =  Lz/2.0
        self.plateBottom = -Lz/2.0

        self.box = [L,L,self.plateTop + particleDiameter*padding - self.plateBottom]

        self.logger.debug(f"[BoundsPlates] Bounds box, box size : {L},{L},{Lz}")
        self.logger.debug(f"[BoundsPlates] Recomputed concentration {nParticles/(L*L*Lz)}")

    def getSimulationBox(self):
        return self.box

    def getSimulationBounds(self):
        return {"plateTop":self.plateTop,"plateBottom":self.plateBottom}

    def check(self,position):

        boxX,boxY,_ = [b/2.0 for b in self.box]

        x,y,z = position

        zSup    = self.plateTop - 1.05*self.particleDiameter
        zBottom = self.plateBottom + 1.05*self.particleDiameter

        if (x>boxX or y>boxY or z>zSup or x<-boxX or y<-boxY or z<zBottom):
            return False

        return True

