__author__ = 'Administrator'

from PIL import Image, ImageDraw

#[[a, b, t], []...]




def gen_sortnet(n, start):
    def copy_net(net, dy, dt=0):
        net2 = [v[:] for v in net]
        for v in net2:
            v[0] += dy
            v[1] += dy
            v[2] += dt
        return net2

    def gen_halfclean(n, start):
        D = []
        for i in range(n/2):
            D.append([i, i+n/2, start+i])
        return D

    def gen_bitonic(n, start):
        if n == 2:
            return gen_halfclean(n, start)
        else:
            L = gen_halfclean(n, start)
            R1 = gen_bitonic(n/2, start+n/2)
            R2 = copy_net(R1, n/2)
            return L + R1 + R2

    def gen_right(n, start):
        L = []
        for i in range(n/2):
            L.append([i, n-i-1, start+i])
        R1 = gen_bitonic(n/2, start+n/2)
        R2 = copy_net(R1, n/2)

        return L + R1 + R2

    if n == 2:
        return gen_halfclean(n, start)

    L1 = gen_sortnet(n/2, 0)
    maxt = 0
    for v in L1:
        maxt = max(maxt, v[2])
    L1 = copy_net(L1, 0, start-1-maxt-1)

    L2 = copy_net(L1, n/2)

    R = gen_right(n, start)

    return L1 + L2 + R

def sortnet(n):
    net = gen_sortnet(n, 0)
    mint = 9999999
    for v in net:
        mint = min(v[2], mint)
    for v in net:
        v[2] -= mint
    R = {}
    for v in net:
        if v[2] not in R:
            R[v[2]] = []
        R[v[2]].append((v[0], v[1]))
    return R




def draw_net(N):
    data = sortnet(N)
    maxt = max(data.keys())

    width = 640
    height = 480

    dx = width/(maxt+2)
    dy = height/(N+1)

    width = dx * (maxt+2)
    height = dy * (N+1)

    img = Image.new('RGB', (width, height), '#ffffff')
    draw = ImageDraw.Draw(img)



    for i in range(N):
        draw.line([(0, dy*(1+i)), (width, dy*(1+i))], width=1, fill='#000000')

    for k, L in data.items():
        for v in L:
            x = (k+1)*dx
            y1 = (v[0]+1)*dy
            y2 = (v[1]+1)*dy
            draw.line([(x, y1), (x, y2)], width=1, fill='#000000')
            r = 2
            draw.ellipse((x-r, y1-r, x+r, y1+r), fill='#000000')
            draw.ellipse((x-r, y2-r, x+r, y2+r), fill='#000000')

    del draw
    img.show()
    img.save('net{0}.jpg'.format(N))


draw_net(16)