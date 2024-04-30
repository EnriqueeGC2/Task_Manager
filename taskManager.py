import psutil
import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
import time

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Administrador de Tareas")
        
        self.tree = ttk.Treeview(self.root, columns=("Name", "Status", "CPU", "Memory"))
        self.tree.heading("#0", text="PID")
        self.tree.heading("Name", text="Nombre del Proceso")
        self.tree.heading("Status", text="Estado")
        self.tree.heading("CPU", text="Uso de CPU (%)")
        self.tree.heading("Memory", text="Uso de Memoria (%)")
        self.tree.pack(expand=True, fill=tk.BOTH)
        
        self.selected_label = tk.Label(self.root, text="Procesos Seleccionados:")
        self.selected_listbox = tk.Listbox(self.root, width=50, height=5)
        
        self.refresh_button = tk.Button(self.root, text="Actualizar", command=self.refresh_processes)
        self.select_button = tk.Button(self.root, text="Seleccionar Proceso", command=self.select_process)
        self.clear_button = tk.Button(self.root, text="Limpiar Selección", command=self.clear_selection)
        self.fifo_button = tk.Button(self.root, text="Simular FIFO", command=self.run_fifo_simulation)
        self.lifo_button = tk.Button(self.root, text="Simular LIFO", command=self.run_lifo_simulation)
        self.compare_button = tk.Button(self.root, text="Comparar FIFO y LIFO", command=self.compare_fifo_lifo)
        self.kill_button = tk.Button(self.root, text="Finalizar Proceso", command=self.kill_process)
        
        self.selected_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.selected_listbox.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.refresh_button.pack(side=tk.RIGHT, padx=5, pady=5)
        self.select_button.pack(side=tk.RIGHT, padx=5, pady=5)
        self.clear_button.pack(side=tk.RIGHT, padx=5, pady=5)
        self.fifo_button.pack(side=tk.RIGHT, padx=5, pady=5)
        self.lifo_button.pack(side=tk.RIGHT, padx=5, pady=5)
        self.compare_button.pack(side=tk.RIGHT, padx=5, pady=5)
        self.kill_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        self.selected_processes = deque()
    
    def refresh_processes(self):
        self.tree.delete(*self.tree.get_children())
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent', 'status'])
                self.tree.insert("", "end", text=str(pinfo['pid']), values=(pinfo['name'], pinfo['status'], f"{pinfo['cpu_percent']:.2f}", f"{pinfo['memory_percent']:.2f}"))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    
    def select_process(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_pid = int(self.tree.item(selected_item)['text'])
            selected_name = self.tree.item(selected_item)['values'][0]
            if selected_pid not in [pid for pid, _ in self.selected_processes]:
                self.selected_processes.append((selected_pid, selected_name))
                self.selected_listbox.insert(tk.END, f"{selected_pid}: {selected_name}")
            else:
                messagebox.showinfo("Seleccionar Proceso", "Este proceso ya ha sido seleccionado.")
    
    def clear_selection(self):
        self.selected_processes.clear()
        self.selected_listbox.delete(0, tk.END)
    
    def run_fifo_simulation(self):
        if not self.selected_processes:
            messagebox.showinfo("Simular FIFO", "No hay procesos seleccionados para simular.")
            return
        
        fifo_window = tk.Toplevel(self.root)
        fifo_window.title("Simulación FIFO")
        fifo_window.geometry("300x200")
        
        fifo_label = tk.Label(fifo_window, text="Simulación FIFO")
        fifo_label.pack(pady=10)
        
        process_label = tk.Label(fifo_window, text="Procesos Seleccionados:")
        process_label.pack(pady=5)
        
        process_listbox = tk.Listbox(fifo_window, width=30, height=5)
        process_listbox.pack(pady=5)
        for pid, name in self.selected_processes:
            process_listbox.insert(tk.END, f"{pid}: {name}")
        
        while self.selected_processes:
            pid, name = self.selected_processes.popleft()
            try:
                process = psutil.Process(pid)
                fifo_label.config(text=f"Ejecutando proceso FIFO {pid}: {name}")
                messagebox.showinfo("Ejecutar Proceso", f"Se ha ejecutado el proceso FIFO {pid}: {name}")
                process_listbox.delete(0, tk.END)
                for pid, name in self.selected_processes:
                    process_listbox.insert(tk.END, f"{pid}: {name}")
                fifo_window.update()
                time.sleep(1)  # Simulación de tiempo de ejecución
            except psutil.NoSuchProcess:
                pass

        messagebox.showinfo("Simular FIFO", "La simulación FIFO ha finalizado.")
        fifo_window.destroy()
    
    def run_lifo_simulation(self):
        if not self.selected_processes:
            messagebox.showinfo("Simular LIFO", "No hay procesos seleccionados para simular.")
            return
        
        lifo_window = tk.Toplevel(self.root)
        lifo_window.title("Simulación LIFO")
        lifo_window.geometry("300x200")
        
        lifo_label = tk.Label(lifo_window, text="Simulación LIFO")
        lifo_label.pack(pady=10)
        
        process_label = tk.Label(lifo_window, text="Procesos Seleccionados:")
        process_label.pack(pady=5)
        
        process_listbox = tk.Listbox(lifo_window, width=30, height=5)
        process_listbox.pack(pady=5)
        for pid, name in self.selected_processes:
            process_listbox.insert(tk.END, f"{pid}: {name}")
        
        while self.selected_processes:
            pid, name = self.selected_processes.pop()
            try:
                process = psutil.Process(pid)
                lifo_label.config(text=f"Ejecutando proceso LIFO {pid}: {name}")
                messagebox.showinfo("Ejecutar Proceso", f"Se ha ejecutado el proceso LIFO {pid}: {name}")
                process_listbox.delete(0, tk.END)
                for pid, name in self.selected_processes:
                    process_listbox.insert(tk.END, f"{pid}: {name}")
                lifo_window.update()
                time.sleep(1)  # Simulación de tiempo de ejecución
            except psutil.NoSuchProcess:
                pass

        messagebox.showinfo("Simular LIFO", "La simulación LIFO ha finalizado.")
        lifo_window.destroy()
    
    def compare_fifo_lifo(self):
        if not self.selected_processes:
            messagebox.showinfo("Comparar FIFO y LIFO", "No hay procesos seleccionados para comparar.")
            return
        
        compare_window = tk.Toplevel(self.root)
        compare_window.title("Comparación FIFO y LIFO")
        compare_window.geometry("600x200")
        
        fifo_frame = tk.Frame(compare_window)
        fifo_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        fifo_label = tk.Label(fifo_frame, text="Simulación FIFO")
        fifo_label.pack(pady=10)
        
        fifo_listbox = tk.Listbox(fifo_frame, width=30, height=5)
        fifo_listbox.pack(pady=5)
        for pid, name in self.selected_processes:
            fifo_listbox.insert(tk.END, f"{pid}: {name}")
        
        lifo_frame = tk.Frame(compare_window)
        lifo_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        lifo_label = tk.Label(lifo_frame, text="Simulación LIFO")
        lifo_label.pack(pady=10)
        
        lifo_listbox = tk.Listbox(lifo_frame, width=30, height=5)
        lifo_listbox.pack(pady=5)
        for pid, name in reversed(self.selected_processes):
            lifo_listbox.insert(tk.END, f"{pid}: {name}")

    def kill_process(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_pid = int(self.tree.item(selected_item)['text'])
            try:
                process = psutil.Process(selected_pid)
                process.terminate()
                messagebox.showinfo("Finalizar Proceso", "El proceso se ha finalizado exitosamente.")
                self.refresh_processes()
            except psutil.NoSuchProcess:
                messagebox.showerror("Error", "No se pudo encontrar el proceso seleccionado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
