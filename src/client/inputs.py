import pygame

class DisplayInput:
    def getInputs(self, inputs):
        cameraSpeed = 5
        quit = False
    #    inputs = COInput()
        inputs.wc = self.resolution[0]
        inputs.hc = self.resolution[1]
        
	if pygame.key.get_pressed()[ pygame.K_UP ]: # up
            inputs.yc = inputs.yc + cameraSpeed

	if pygame.key.get_pressed()[ pygame.K_DOWN ]: # down
            inputs.yc = inputs.yc - cameraSpeed

	if pygame.key.get_pressed()[ pygame.K_RIGHT ]: # right
            inputs.xc = inputs.xc + cameraSpeed

	if pygame.key.get_pressed()[ pygame.K_LEFT ]: # left
            inputs.xc = inputs.xc - cameraSpeed

        self.camera = (inputs.xc,inputs.yc)

	e = pygame.event.poll()
	while e.type != pygame.NOEVENT:
		if e.type == pygame.QUIT or \
		  ( e.type == pygame.KEYUP and e.key == 113 ):
		    quit = True
		elif e.type == pygame.MOUSEBUTTONDOWN:
                    inputs.mouseDownAt = e.pos
                    inputs.mouseDownAtV = self.getVirtualPos( e.pos )
		elif e.type == pygame.MOUSEBUTTONUP:
                    inputs.mouseUpAt = e.pos
                    inputs.mouseUpAtV = self.getVirtualPos( e.pos )
                    inputs.mouseUpped = True

		e = pygame.event.poll()

        return (quit, inputs)

