from multiprocessing import Process, Queue
import subprocess
import sys
import threading
import select
import time


class PDFViewerProcess:
    
    def terminate(self):
        
        self.terminate_event.set()
        #self.output_thread.join()
        #self.flag_thread.join()
        self.cleanup()

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

        
        
        #self.output_thread.join()
        #self.flag_thread.join()
        

        

        '''   
        while not self.output_flag:   
            self.cleanup()
            self.flag_thread.start()
            self.output_thread.start()
        '''
        

    def send_flags(self):
        while True:
            if self.proc.poll() is not None:
                break

            if not self.q.empty():
                flag = self.q.get()
                self.proc.stdin.write(flag + '\n')
                self.proc.stdin.flush()
                print(f'Sent flag: {flag}')
                self.proc.wait()
                
                #self.proc.communicate()
                #time.sleep(0)
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
        self.pause_event.set()
        while True:
            # Check if there's a message from the subprocess
            if self.proc.poll() is not None:
                break
            
            self.output = self.proc.stdout.readline().strip()
            self.proc.stdout.flush()

            
            if self.output:
                print(f'Received flag: {self.output}')
                self.handle_output()
                time.sleep(0)
                '''
                if self.output_flag:
                    break'''
                
        
    def load_output_process(self):
        #print("Output thread finished")
        if self.pause_event.is_set():
            print("process:",self.proc.poll())
            if self.output_flag:
                if self.output == '<Left>':
                    self.prev_page()
                elif self.output == '<Right>':
                    self.next_page()
                elif self.output == '<Escape>':
                    self.slideshow_process = False
                    #self.slideshow_mode = True
                    self.slideshow_housekeep()
                elif self.output == 'LOAD':
                    self.show_page()

            self.output_flag = False
            self.pause_event.clear()
        #self.cleanup()
                
    def cleanup(self):
        
        if self.proc and self.proc.poll() is not None:
            self.proc.terminate()
            self.proc.wait()
            print("Subprocess terminated.")
        

        if self.output_thread and self.output_thread.is_alive():
            self.output_thread.join()
            print("Output thread finished")

        if self.flag_thread and self.flag_thread.is_alive():
            self.flag_thread.join()
            print("Flag thread finished")

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

        print(self.output_flag)
        self.root.after(1,self.load_output_process)

        
            
            

    