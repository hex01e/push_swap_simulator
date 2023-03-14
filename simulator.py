#!/usr/bin/python3
from tkinter import *
import numpy as np
import os, time, subprocess , sys

win = Tk()
win.geometry("1015x900")
win.title("push_swap simulator")
win.resizable(width=False, height=False)
v = StringVar()
l = StringVar()
ops = 0
index = 0
size_n = 0
max_n = 0
min_n = 0
tmp_speed = 2
yes = 0
speed = 0
backup = []
stack_a = []
stack_b = []
push_swap = []
done = 0
def get_started():
	global size_n, max_n, min_n, stack_a, stack_b, v , ops , push_swap, backup, index, speed
	if len(sys.argv) != 2:
		print("Usage : ./viz.py [path of push_swap program]")
		exit(1)
	size_n = int(size_i.get())
	max_n = int(maxx_i.get())
	min_n = int(minn_i.get())
	if size_n > 1 and max_n > min_n:
		generate()
	else:
		v.set("size > 1 | max > min")


def restart():
	global stack_a , stack_b, ops, backup,speed,push_swap,yes,done
	speed = 0
	stack_a = [i for i in backup]
	stack_b = []
	ops = 0
	yes  = 1
	done = 0
	redraw()
	run()

def generate():
	global size_n, max_n, min_n, stack_a, stack_b, push_swap, backup, ops, speed, yes, done, l
	size_n = int(size_i.get())
	max_n = int(maxx_i.get())
	min_n = int(minn_i.get())
	stack_a = [int(num) for num in np.random.randint(min_n,max_n,size_n)]
	stack_a = list(dict.fromkeys(stack_a))
	if sys.argv[1] != "-n":
		push_swap = subprocess.check_output([sys.argv[1]] + [str(i) for i in stack_a], stderr=subprocess.STDOUT,
							timeout=12).splitlines()
	l.set("instructions count: " + str(len(push_swap)))
	stack_b = []
	ops = 0
	speed = 0
	yes = 1
	done = 0
	backup = [i for i in stack_a]
	run_btn.config(text='run')
	redraw()

def speedup():
	global speed
	if speed > 0.00012967236152753247:
		speed /= 4


def speeddown():
	global speed
	if speed < 1:
		speed *= 0.4
	if speed < 2:
		speed *= 4

# def color(i):
#	 c = int(i) * 0xfe01 + 0xff
#	 col = '#' + '{:06x}'.format(int(c/255))
#	 return col

def median(li):
	list = [i for i in li]
	list.sort()
	return list[int(len(list)/2)]

def redraw():
	global stack_a, stack_b, ops, med
	draws.delete('all')
	w = (abs(max(stack_a + stack_b)) + abs(min(stack_a + stack_b)))/300
	h = 900 / size_n - 1/size_n
	med = median(stack_a + stack_b)
	mx = max(stack_a + stack_b)
	mn = min(stack_a + stack_b)
	mxb, mnb , medb = 0,0,0
	if len(stack_a)> 0:
		meda = median(stack_a)
		mxa = max(stack_a)
		mna = min(stack_a)
	y = 0
	o = 0
	for i in stack_a:
		if len(stack_a) > 0:
			o = (i - min(stack_a + stack_b))/(max(stack_a + stack_b) - min(stack_a + stack_b))
		else:
			o = 1
		draws.create_rectangle(0, y, (i +abs(min(stack_a + stack_b)))/w + 10 + 30 ,y + h, fill=set_color(o), outline="")
		y += h
	y = 0
	mxb, mnb , medb = 0,0,0
	if len(stack_b) > 0:
		medb = median(stack_b)
		mxb = max(stack_b)
		mnb = min(stack_b)
	for i in stack_b:
		if len(stack_b) > 0:
			o = (i - min(stack_a + stack_b))/(max(stack_a + stack_b) - min(stack_a + stack_b))
		else:
			o = 1
		draws.create_rectangle(450, y, (i +abs(min(stack_a + stack_b)))/w + 10 + 450,y + h, fill=set_color(o), outline="")
		y += h
	v.set("current :" + str(ops))
	draws.update()

def set_color(index):
	col = '#%02x%02x%02x' % (int(255 * (index - 0.3) * (index > 0.3)),
							 int(255 * index
								 - ((510 * (index - 0.6)) * (index > 0.6))),
							 int((255 - 510 * index) * (index < 0.5)))
	return col

def _pa():
	global stack_a , stack_b, ops
	if len(stack_b) >= 1:
		stack_a = [stack_b[0]] + stack_a
		del stack_b[0]
		ops += 1
		redraw()

def _pb():
	global stack_a , stack_b, ops
	if len(stack_a) >= 1:
		stack_b = [stack_a[0]] + stack_b
		del stack_a[0]
		ops += 1
		redraw()

def _sa():
	global stack_a, ops
	if len(stack_a) >= 2:
		stack_a[0], stack_a[1] = stack_a[1], stack_a[0]
		ops += 1
		redraw()

def _sb():
	global stack_b, ops
	if len(stack_b) >= 2:
		stack_b[0], stack_b[1] = stack_b[1], stack_b[0]
		ops += 1
		redraw()

def _ss():
	global stack_a , stack_b, ops
	if len(stack_b) >= 2 and len(stack_a) >= 2:
		stack_a[0], stack_a[1] = stack_a[1], stack_a[0]
		stack_b[0], stack_b[1] = stack_b[1], stack_b[0]
		ops += 1
		redraw()

def _ra():
	global stack_a, ops
	if len(stack_a) >= 2:
		stack_a.append(stack_a[0])
		del stack_a[0]
		ops += 1
		redraw()

def _rb():
	global stack_b, ops
	if len(stack_b) >= 2:
		stack_b.append(stack_b[0])
		del stack_b[0]
		ops += 1
		redraw()

def _rr():
	global stack_a , stack_b, ops
	if len(stack_b) >= 2 and len(stack_a) >= 2:
		stack_a.append(stack_a[0])
		del stack_a[0]
		stack_b.append(stack_b[0])
		del stack_b[0]
		ops += 1
		redraw()

def _rra():
	global stack_a, ops
	if len(stack_a) >= 2:
		stack_a = [stack_a[-1]] + stack_a
		del stack_a[-1]
		ops += 1
		redraw()

def _rrb():
	global stack_b, ops
	if len(stack_b) >= 2:
		stack_b = [stack_b[-1]] + stack_b
		del stack_b[-1]
		ops += 1
		redraw()

def _rrr():
	global stack_a , stack_b, ops
	if len(stack_b) >= 2 and len(stack_a) >= 2:
		stack_a = [stack_a[-1]] + stack_a
		del stack_a[-1]
		stack_b = [stack_b[-1]] + stack_b
		del stack_b[-1]
		ops += 1
		redraw()

def runn():
	global stack_a , stack_b, ops, speed, index, yes, done
	if yes:
		index = 0
		yes = 0
	while index < len(push_swap) and not done:
		if speed != 0:
			if push_swap[index] == b'pa':
				_pa()
			elif push_swap[index] == b'pb':
				_pb()
			elif push_swap[index] == b'ra':
				_ra()
			elif push_swap[index] == b'rb':
				_rb()
			elif push_swap[index] == b'rr':
				_rr()
			elif push_swap[index] == b'rra':
				_rra()
			elif push_swap[index] == b'rrb':
				_rrb()
			elif push_swap[index] == b'rrr':
				_rrr()
			elif push_swap[index] == b'sa':
				_sa()
			elif push_swap[index] == 'sb':
				_sb()
			elif push_swap[index] == b'ss':
				_ss()
			time.sleep(speed * 0.15)
			index+=1
		else:
			return
	done = 1
	index = 0
	speed = 0
	run_btn.config(text='run')

def run():
	global tmp_speed, speed, index, push_swap
	if len(push_swap) != index:
		if speed != 0:
			tmp_speed = speed
			speed = 0
			run_btn.config(text='run')
		else:
			speed = tmp_speed
			run_btn.config(text='stop')
			runn()

main = Frame(win, height=900, width=1015, bd=0)
main.pack()

draws = Canvas(main, bg='black', height=900, width=800, highlightthickness=0)
draws.pack(side = LEFT)

# a_text = Label(draws,width=7,height=1,text="stack a",bg='black',fg='white')
# a_text.place(x=150,y=455)

# a_text = Label(draws,width=7,height=1,text="stack b",bg='black',fg='white')
# a_text.place(x=356,y=455)

instr = Frame(main,height=900,width=210)
instr.pack(side = RIGHT)

push = Frame(instr,height=50,width=210)
push.grid(row=0)
pa = Button(push,width=7,height=1,text="pa",command=_pa)
pa.pack(side=LEFT)
pb = Button(push,width=7,height=1,text="pb",command=_pb)
pb.pack(side=RIGHT)

swap = Frame(instr,height=50,width=210)
swap.grid(row=1)
sa = Button(swap,width=7,height=1,text="sa",command=_sa)
sa.pack(side=LEFT)
sb = Button(swap,width=7,height=1,text="sb",command=_sb)
sb.pack(side=RIGHT)

ss = Button(instr,width=18,height=1,text="ss",command=_ss)
ss.grid(row=2)

rotate = Frame(instr,height=50,width=210)
rotate.grid(row=3)
sa = Button(rotate,width=7,height=1,text="ra",command=_ra)
sa.pack(side=LEFT)
sb = Button(rotate,width=7,height=1,text="rb",command=_rb)
sb.pack(side=RIGHT)

rr = Button(instr,width=18,height=1,text="rr",command=_rr)
rr.grid(row=4)

rrotate = Frame(instr,height=50,width=210)
rrotate.grid(row=5)
sa = Button(rrotate,width=7,height=1,text="rra",command=_rra)
sa.pack(side=LEFT)
sb = Button(rrotate,width=7,height=1,text="rrb",command=_rrb)
sb.pack(side=RIGHT)

rr = Button(instr,width=18,height=1,text="rrr",command=_rrr)
rr.grid(row=6)

size = Frame(instr,height=50,width=210)
size.grid(row=7)
size_text = Label(size,width=7,height=1,text="size")
size_text.pack(side=LEFT)
size_i = Entry(size,width=7)
size_i.insert(0, "100")
size_i.pack(side=RIGHT)

maxx = Frame(instr,height=50,width=210)
maxx.grid(row=8)
maxx_text = Label(maxx,width=7,height=1,text="max")
maxx_text.pack(side=LEFT)
maxx_i = Entry(maxx,width=7)
maxx_i.insert(0, "5000")
maxx_i.pack(side=RIGHT)

minn = Frame(instr,height=50,width=210)
minn.grid(row=9)
minn_text = Label(minn,width=7,height=1,text="min")
minn_text.pack(side=LEFT)
minn_i = Entry(minn,width=7)
minn_i.insert(0, "-5000")
minn_i.pack(side=RIGHT)

sp = Frame(instr,height=50,width=210)
sp.grid(row=10)
sp_up = Button(sp,width=3,height=1,text="speed+",command=speedup)
sp_up.pack(side=LEFT)
run_btn = Button(sp,width=3,height=1,text="run",command=run)
run_btn.pack(side=LEFT)
sp_down = Button(sp,width=3,height=1,text="speed-",command=speeddown)
sp_down.pack(side=LEFT)

st = Frame(instr,height=50,width=210)
st.grid(row=11)
start = Button(st,width=7,height=1,text="generate",command=generate)
start.pack(side=LEFT)
reset = Button(st,width=7,height=1,text="restart",command=restart)
reset.pack(side=RIGHT)

ops_count = Label(instr,textvariable=l)
ops_count.grid(row=13)

ops_count = Label(instr,textvariable=v)
ops_count.grid(row=14)

get_started()

mainloop()
