
car is a named tuple with (pos, vel, model)

circle track has a radius that is translated to length, which is wrapped arpound
so that car.move() will do x_next = x_next % track_length

Then cars need to be assigned a leader, might work with a circular list

check lookahead, then decide to adjust speed?

Cars and models have functionality to be update for 1 step
pygame takes care of running a game loop where steps are executed
maybe matplotib animation pack too
