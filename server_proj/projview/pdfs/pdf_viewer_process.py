from multiprocessing import Process, Queue, Array
import ctypes
import subprocess
import sys
import threading
import select
import time
import tkinter


class PDFViewerProcess:
    
    def terminate(self):
        
        for thread in threading.enumerate():
            print("Cleaning:",thread.getName())
        
        self.terminate_event.clear()
        #self.output_thread.join()
        #self.flag_thread.join()
        self.cleanup()
        for thread in threading.enumerate():
            print("Clean Reamaining:",thread.getName())
        self.terminate_event.clear()

    def slide_process(self):

        
        '''
        if not self.q.empty():
                    # Send a flag to the subprocess
                self.flag = self.q.get()
                self.proc.stdin.write((self.flag + '\n').encode())
                self.proc.stdin.flush()
                print(f'Sent flag: {self.flag}')   

        #Start a thread to handle the output from the subprocess
        self.output_thread = threading.Thread(target=self.read_output)
        self.output_thread.daemon = True
        self.output_thread.start()
        print("Output thread started")

        self.cleanup()
        
        '''
        self.pause_event = threading.Event()
        self.pause_event.set()
        
        #Start a thread to handle the output from the subprocess
        self.output_thread = threading.Thread(target=self.read_output)
        self.output_thread.daemon = True
        self.output_thread.start()

        # Start a thread to send flags to the subprocess
        self.flag_thread = threading.Thread(target=self.send_flags)
        self.flag_thread.daemon = True
        self.flag_thread.start()
        
        self.coord_thread = threading.Thread(target=self.send_coords)
        self.coord_thread.daemon = True
        self.coord_thread.start()
        



        
        


    def send_coords(self):
        print(threading.current_thread().getName())
        while self.proc is not None:
            while not self.terminate_event.is_set():
                if self.proc.poll() is not None:
                    break

                with self.coord_condition:
                    while  list(self.pointer_position) == [9999,9999] and not self.terminate_event.is_set():
                        self.coord_condition.wait()

                    if self.terminate_event.is_set():
                        break

                    coord = list(self.pointer_position)
                    coord_str = ' '.join(str(e) for e in coord)
                    self.proc.stdin.write(coord_str + '\n')
                    self.proc.stdin.flush()
                    print(f'Sent coord: {coord_str}')
                    self.pointer_position = Array(ctypes.c_int, [9999, 9999]) #9999 signifies empty array

                    print("Done")
                    
                    #self.proc.communicate()
                    #time.sleep(0)
                    #self.cleanup()

            


        

        '''   
        while not self.output_flag:   
            self.cleanup()
            self.flag_thread.start()
            self.output_thread.start()
        '''
        
    def handle_new_flag(self, flag):
        with self.flag_condition:
            self.q.put(flag)
            self.flag_condition.notify()

        

    def send_flags(self):
        print(threading.current_thread().getName())
        while self.proc is not None:
            while not self.terminate_event.is_set():
                if self.proc.poll() is not None:
                    break

                
                print("Test",threading.current_thread().getName())
                with self.flag_condition:
                    while self.q.empty() and not self.terminate_event.is_set():
                        self.flag_condition.wait()

                    if self.terminate_event.is_set():
                        break

                    flag = self.q.get()
                
                    self.proc.stdin.write(flag + '\n')
                    self.proc.stdin.flush()
                    print(f'Sent flag: {flag}')
                    #self.flag_thread.join()
                    #self.proc.wait()
                    #self.proc.communicate()
                    print("Done")
                    #time.sleep(0)
                    
                if self.proc.poll() is not None:
                    break  
                
                    #
                    #time.sleep(0)
                    #self.cleanup()
            #self.cleanup()
        
            

        '''
        try: 
            while True:
                
                if not self.output_flag:
                    self.output_thread.start()
                    print("Output thread started")
                if self.proc.poll() is not None:
                    break  # subprocess has ended

                if not self.q.empty():
                    # Send a flag to the subprocess
                    flag = self.q.get()

                    #self.ready = self.proc.stdin in select.select([self.proc.stdin], [], [])[0]
                    #print(self.ready)
                    
                    self.proc.stdin.write((flag + '\n').encode())
                    self.proc.stdin.flush()
                    self.proc.communicate()

                    print(f'Sent flag: {flag}',self.proc.poll())
                    self.proc.wait()
                    break

                if self.output_flag:
                    if self.output == '<Left>':
                        self.prev_page()
                        break
                    elif self.output == '<Right>':
                        self.next_page()
                        break
                    elif self.output == '<Escape>':
                        self.slideshow_process = False
                        self.toggle_slideshow()
                        break
                    elif self.output == 'LOAD':
                        self.show_page()
                        break

                    
                    
                    

            #self.proc.communicate()
            #self.cleanup()


            

        except KeyboardInterrupt:
            pass
        finally:
            # Ensure the subprocess is terminated
            self.cleanup()
        '''


        
        



    def read_output(self):
        self.output = None
        self.output_flag = False
        self.pause_event.wait()
        while True:
            while self.proc is not None:
                # Check if there's a message from the subprocess
                if self.proc.poll() is not None:
                    break
                
                self.output = self.proc.stdout.readline().strip()
                self.proc.stdout.flush()

                
                if self.output:
                    print(f'Received flag: {self.output}')
                    self.handle_output()
                    #time.sleep(0)
                    '''
                    if self.output_flag:
                        break'''
                
        
    def load_output_process(self):
        print("Undertaking Action....")
        
        if threading.current_thread().getName() != 'MainThread':
            return
        print(threading.current_thread().getName())
        if self.pause_event.is_set():
            print("Sub-process Error:",self.proc.poll())
            if self.output_flag:
                if self.output == '<Left>':
                    self.prev_page()
                elif self.output == '<Right>':
                    self.next_page()
                elif self.output == '<Escape>':
                    print("SlideShow Terminated")
                    
                    self.slideshow_process = False
                    self.slideshow_active = False
                    self.pointer_button.config(state=tkinter.DISABLED)
                    self.toggle_pointer()
                    
                    self.pause_event.clear()
                    self.slideshow_housekeep()
                elif self.output == 'LOAD':
                    print("SlideShow Active")
                    self.slideshow_active = True
                    self.pointer_button.config(state=tkinter.NORMAL)

            self.output_flag = False
            
        #self.cleanup()
                
    def cleanup(self):
        while self.proc is not None and self.subprocess_active:
            self.terminate_event.set() 
            print(threading.current_thread().getName())
            self.proc.terminate()
            
            self.proc.wait()
            print("Subprocess terminated.")
            self.subprocess_active = False
            
            #if self.proc and self.proc.poll() is None:
            self.output_thread.join()
            print("Output thread finished")  

            with self.flag_condition:
                self.flag_condition.notify()
            self.flag_thread.join()
            #time.sleep(0)
            print("Flag thread finished")

            with self.coord_condition:
                self.coord_condition.notify()
            self.coord_thread.join()
            print("Pointer thread finished")


            self.terminate_event.clear()

        #if self.output_thread and self.output_thread.is_alive():
            
        

        #if self.flag_thread and self.flag_thread.is_alive():
            #self.condition.clear()
            

        '''
        if self.coord_thread and self.coord_thread.is_alive():
            self.coord_thread.join()
            print("Coord thread finished")'''

    '''
    def start(self):
        # Send a flag to slide.py
        self.q.put('START')

    def stop(self):
        # Send another flag to slide.py
        self.q.put('STOP')

    def join(self):
        # Wait for slide.py to finish
        self.p.join()
        '''

    def handle_output(self):
        # Check if there's a message from the subprocess
        if self.output == '<Left>':
            self.output_flag = True
            self.pause_event.set()
            
        elif self.output == '<Right>':
            self.output_flag = True
            self.pause_event.set()
            
        elif self.output == '<Escape>':
            self.output_flag = True
            self.pause_event.set()
            #print("Escape flag received")
            
        elif self.output == 'LOAD':
            self.output_flag = True
            self.pause_event.set()
            
            
        else:
            #print(f'Unknown flag: {self.output}')
            self.output_flag = False

        print("Action Received:", self.output_flag)
        if(self.output_flag):
            print(self.output_thread.getName())
            print("Done loading")
            self.root.after(0,self.load_output_process)

        return
            

        
        
        

        
            
            

    