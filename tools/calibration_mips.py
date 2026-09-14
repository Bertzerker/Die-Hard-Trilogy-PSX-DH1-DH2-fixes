"""Title-screen calibration code, tested in DuckStation.

Uses SDK diagnostic-string scratch ranges identified in the original Nuvee
patch notes. Exhaustive diagnostic/error-path reference auditing remains outstanding.
"""
import struct

STATE=0x800893E0
INPUT=0x80088BF0
SCREEN=0x80088F20
TEXT=0x80089380

REG={n:i for i,n in enumerate('zero at v0 v1 a0 a1 a2 a3 t0 t1 t2 t3 t4 t5 t6 t7 s0 s1 s2 s3 s4 s5 s6 s7 t8 t9 k0 k1 gp sp fp ra'.split())}

class Asm:
    def __init__(self,base):self.base=base;self.w=[];self.labels={};self.fix=[]
    def label(self,n):self.labels[n]=len(self.w)
    def i(self,op,t,s,k):self.w.append(op<<26|REG[s]<<21|REG[t]<<16|(k&65535))
    def r(self,fn,d,s,t='zero'):self.w.append(REG[s]<<21|REG[t]<<16|REG[d]<<11|fn)
    def li(self,t,k):self.i(13,t,'zero',k)
    def addr(self,t,k):self.i(15,t,'zero',k>>16);self.i(13,t,t,k&65535)
    def add(self,t,s,k):self.i(9,t,s,k)
    def lw(self,t,k,s):self.i(35,t,s,k)
    def lh(self,t,k,s):self.i(33,t,s,k)
    def lhu(self,t,k,s):self.i(37,t,s,k)
    def sw(self,t,k,s):self.i(43,t,s,k)
    def sh(self,t,k,s):self.i(41,t,s,k)
    def mov(self,d,s):self.r(33,d,s)
    def nop(self):self.w.append(0)
    def branch(self,op,s,t,n):self.fix.append((len(self.w),n));self.i(op,t,s,0)
    def b(self,n):self.branch(4,'zero','zero',n)
    def call(self,a):self.w.append(0x0C000000|((a>>2)&0x3ffffff))
    def jump(self,a):self.w.append(0x08000000|((a>>2)&0x3ffffff))
    def finish(self,limit):
        for i,n in self.fix:self.w[i]|=(self.labels[n]-i-1)&65535
        b=struct.pack('<%dI'%len(self.w),*self.w)
        assert len(b)<=limit,(hex(self.base),len(b),limit)
        return b

def build():
    # Hook before the original button-remapping block. Original, uncorrected
    # converted coordinates are already stored in the pad buffer at this point.
    a=Asm(INPUT)
    a.addr('t8',STATE)
    a.lhu('a1',2,'v1');a.lh('a3',8,'v1');a.sw('a1',4,'t8')
    a.sw('a3',8,'t8');a.lh('a1',6,'v1');a.nop();a.sw('a1',12,'t8')
    a.branch(4,'a3','zero','remap');a.nop() # offscreen remains (0,0)
    a.lw('a1',16,'t8');a.nop();a.r(33,'a3','a3','a1');a.sh('a3',8,'v1')
    a.lh('a3',6,'v1');a.lw('a1',20,'t8');a.nop()
    a.r(33,'a3','a3','a1');a.sh('a3',6,'v1')
    a.label('remap');a.lw('a3',0,'t8');a.lhu('a1',2,'v1')
    a.branch(4,'a3','zero','buttons');a.nop()
    a.li('a1',65535) # consume all buttons during calibration
    a.label('buttons');a.jump(0x80088EAC);a.li('a3',65535)
    input_code=a.finish(0x230)

    a=Asm(SCREEN)
    a.add('sp','sp',-56);a.sw('ra',52,'sp');a.sw('s0',48,'sp')
    a.addr('s0',STATE)
    a.addr('t0',0x800B6B70);a.lh('t0',0,'t0');a.li('t1',4)
    a.branch(5,'t0','t1','disconnect');a.nop()
    a.lw('t0',0,'s0');a.lw('t1',4,'s0');a.nop()
    a.branch(5,'t0','zero','active');a.i(12,'t2','t1',8)
    a.branch(5,'t2','zero','normal');a.li('t0',1)
    a.sw('t0',0,'s0')
    a.label('active')
    # B / Start cancels, then waits for release like a completed calibration.
    a.i(12,'t2','t1',0x4000);a.branch(5,'t2','zero','phase');a.nop()
    a.li('t0',3);a.sw('t0',0,'s0')
    a.label('phase');a.li('t2',2);a.branch(4,'t0','t2','aim');a.nop()
    a.i(12,'t2','t1',0x6008);a.li('t3',0x6008)
    a.branch(5,'t2','t3','draw');a.li('t2',1)
    a.branch(5,'t0','t2','complete');a.li('t0',2)
    a.sw('t0',0,'s0');a.b('draw');a.nop()
    a.label('complete');a.sw('zero',0,'s0');a.b('normal');a.nop()
    a.label('aim');a.i(12,'t2','t1',0x2000)
    a.branch(5,'t2','zero','draw');a.nop()
    a.lw('t2',8,'s0');a.lw('t3',12,'s0')
    a.branch(4,'t2','zero','invalid');a.nop()
    # Title renderer's coordinate center is (256,120), verified at 512x240.
    a.li('t0',256);a.r(35,'t2','t0','t2');a.li('t0',120)
    a.r(35,'t3','t0','t3');a.sw('t2',16,'s0');a.sw('t3',20,'s0')
    a.li('t0',3);a.sw('t0',0,'s0');a.b('draw');a.nop()
    a.label('invalid');a.li('t0',1);a.sw('t0',0,'s0')
    a.label('draw')
    # Centered heading and instructions, using the game's initialized font.
    for y,txt in [(60,TEXT),(180,TEXT+24)]:
        a.li('t0',600);a.sw('t0',16,'sp');a.addr('t0',0x800B63E0)
        a.sw('t0',20,'sp');a.sw('t0',24,'sp')
        a.li('a0',256);a.li('a1',y);a.addr('a2',txt)
        a.call(0x80076478);a.li('a3',1800)
    # White rectangular target with an exact center, via game's line helper.
    for off,val in [(32,244),(34,114),(36,268),(38,126)]:
        a.li('t0',val);a.sh('t0',off,'sp')
    a.add('a0','sp',32);a.li('a1',255);a.li('a2',255)
    a.call(0x80046FE0);a.li('a3',255)
    a.lw('ra',52,'sp');a.lw('s0',48,'sp');a.add('sp','sp',56)
    a.jump(0x8004D23C);a.nop() # skip original title and Start/gameplay transition
    a.label('disconnect');a.sw('zero',0,'s0');a.b('restore');a.nop()
    a.label('normal')
    a.li('t0',350);a.sw('t0',16,'sp');a.addr('t0',0x800B63E0)
    a.sw('t0',20,'sp');a.sw('t0',24,'sp')
    a.li('a0',256);a.li('a1',228);a.addr('a2',TEXT+56)
    a.call(0x80076478);a.li('a3',1100)
    a.label('restore');a.lw('ra',52,'sp');a.lw('s0',48,'sp');a.add('sp','sp',56)
    # Replay the displaced instructions; let the original title routine run.
    a.addr('v0',0x800B6CC8);a.lw('v0',0,'v0');a.jump(0x8004D0C0);a.nop()
    screen_code=a.finish(0x3D0)
    text=b'GUN CALIBRATION\0'.ljust(24,b'\0')+b'AIM AT CENTER AND SHOOT\0'
    text=text.ljust(56,b'\0')+b'GRENADE BUTTON: CALIBRATE\0'
    text=text.ljust(96,b'\0')
    def jump(dest):return struct.pack('<II',0x08000000|((dest>>2)&0x3ffffff),0)
    return {
        INPUT:input_code,SCREEN:screen_code,TEXT:text,
        STATE:struct.pack('<II',0,65535)+bytes(56),
        0x80088EA4:jump(INPUT),0x8004D0B8:jump(SCREEN),
        0x80088E94:bytes.fromhex('0001a520'),
        0x80088E9C:bytes.fromhex('edffe720'),
    }

if __name__=='__main__':
    for addr,data in build().items():print(hex(addr),len(data))
