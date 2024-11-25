from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from datetime import datetime
import config  

class ReadOnlyDelegate(QStyledItemDelegate):
    '''
    Function is used to make some rows and columns read only   
    Example :   delegate = ReadOnlyDelegate(self)
                self.edges_table.setItemDelegateForColumn(2,delegate)
    '''
    def createEditor(self, parent, option, index):
        return


def sequence_tab_build(self):
    #SEQUENCE TAB WIDGET
    self.sequence_tab_widget = QWidget()
    self.sequence_lable = QLabel(self.sequence_tab_widget)
    self.sequence_lable.setText("Timing Sequence")
    self.sequence_lable.setFont(QFont('Arial', 14))
    self.sequence_lable.setGeometry(85, 0, 200, 30)
    #file_name label
    self.file_name_lable = QLabel(self.sequence_tab_widget)
    self.file_name_lable.setFont(QFont('Arial', 10))
    self.file_name_lable.setGeometry(275, 2, 600, 30)
    #SEQUENCE TAB LAYOUT
    self.sequence_table = QTableWidget(self.sequence_tab_widget)
    width_of_table = 825
    self.sequence_table.setGeometry(QRect(10, 30, width_of_table, 1020))                                                #size of the table
    sequence_num_columns = 5
    self.sequence_table.setColumnCount(sequence_num_columns)
    self.sequence_table.setRowCount(1)
    self.sequence_table.setHorizontalHeaderLabels(["#", "Name","ID", "Time expression","Time (ms)"])
    self.sequence_table.verticalHeader().setVisible(False)
    self.sequence_table.horizontalHeader().setFixedHeight(60)
    self.sequence_table.horizontalHeader().setFont(QFont('Arial', 12))
    self.sequence_table.setFont(QFont('Arial', 12))
    self.sequence_table.setColumnWidth(0,50)
    self.sequence_table.setColumnWidth(1,220)
    self.sequence_table.setColumnWidth(2,100)
    self.sequence_table.setColumnWidth(3,207)
    self.sequence_table.setColumnWidth(4,246)
    self.sequence_table.itemChanged.connect(self.sequence_table_changed)
    delegate = ReadOnlyDelegate(self)
    self.sequence_table.setItemDelegateForRow(0,delegate)
    self.sequence_table.setItemDelegateForColumn(0,delegate)
    self.sequence_table.setItemDelegateForColumn(2,delegate)
    self.sequence_table.setItemDelegateForColumn(4,delegate)
    #Setting the default values 
    self.sequence_table.setItem(0, 0, QTableWidgetItem("0"))
    self.sequence_table.setItem(0, 1, QTableWidgetItem(self.experiment.sequence[0].name))
    self.sequence_table.setItem(0, 2, QTableWidgetItem(self.experiment.sequence[0].id))
    self.sequence_table.setItem(0, 3, QTableWidgetItem(self.experiment.sequence[0].expression))
    self.sequence_table.setItem(0, 4, QTableWidgetItem(str(self.experiment.sequence[0].value)))
    
    #BUTTONS
    #button to save current sequence
    self.save_sequence_button = QPushButton(self.sequence_tab_widget)
    self.save_sequence_button.setFont(QFont('Arial', 14))
    self.save_sequence_button.setGeometry(width_of_table + 50, 30, 200, 30)
    self.save_sequence_button.setText("Save sequence")
    self.save_sequence_button.clicked.connect(self.save_sequence_button_clicked)
    self.save_sequence_button.setToolTip("Save sequence button saves the experimental description to a file. Everything in the user interface will be saved including the title names, states of scanning table, and all tabs. The only difference will be the logger. It will not be saved. If a sequence was saved or loaded, it will overwrite the open sequence file! Therefore, be careful when pressing this button or you risk loosing the previous state of the experiment.")
    #button to load new sequence
    self.load_sequence_button = QPushButton(self.sequence_tab_widget)
    self.load_sequence_button.setFont(QFont('Arial', 14))
    self.load_sequence_button.setGeometry(width_of_table + 50, 80, 200, 30)
    self.load_sequence_button.setText("Load sequence")
    self.load_sequence_button.clicked.connect(self.load_sequence_button_clicked)
    self.load_sequence_button.setToolTip("Load sequence button allows user to load the presaved sequences. It will load the full state of the experimental sequence leaving the logger at the same state as before loading the sequence. Do save your sequences before loading new ones in order to not lose them. The newly loaded sequence file will be linked with the current state of the Quantrol. By pressing the save sequence button the user can overwrite the loaded sequence!")
    #button to insert edge
    self.insert_edge_button = QPushButton(self.sequence_tab_widget)
    self.insert_edge_button.setFont(QFont('Arial', 14))
    self.insert_edge_button.setGeometry(width_of_table + 50, 180, 200, 30)
    self.insert_edge_button.setText("Insert Edge")
    self.insert_edge_button.clicked.connect(self.insert_edge_button_clicked)
    self.insert_edge_button.setToolTip("Insert edge button inserts an edge in the edge of the sequence with a blank name and time expression exactly the same as the leading edge. All channels parameters will be not be user entered and therefore will display the previously set states. In other words, their changed parameters will be False meaning that they do not require the update of the hardware states at the newly inserted Edge.")
    #button to delete edge
    self.delete_edge_button = QPushButton(self.sequence_tab_widget)
    self.delete_edge_button.setFont(QFont('Arial', 14))
    self.delete_edge_button.setGeometry(width_of_table + 50, 230, 200, 30)
    self.delete_edge_button.setText("Delete Edge")
    self.delete_edge_button.clicked.connect(self.delete_edge_button_clicked)
    self.delete_edge_button.setToolTip("Delete edge button requires the user to choose the edge that needs to be deleted by right clicking it in the Timing Sequence table. It checks if the corresponding ID variable of the edge that needs to be deleted is used anywhere and will not allow deletion in case it is used by showing the first instance it was found to be used at. Otherwise, it deletes the selected edge and updates the Timing Sequence table.")
    
    if config.allow_skipping_images:
        #trigger camera 10 times
        self.skip_images_button = QPushButton(self.sequence_tab_widget)
        self.skip_images_button.setFont(QFont('Arial', 14))
        self.skip_images_button.setGeometry(width_of_table + 50, 330, 200, 30)
        self.skip_images_button.setText("Skip images")
        self.skip_images_button.clicked.connect(self.skip_images_button_clicked)
        self.skip_images_button.setStyleSheet("background-color : green; color : white") 
        self.skip_images_button.setToolTip("Skip images button allows on demand triggering the camera acquisition 10 times in the beginning of experiment. Button's color represents current state where green indicates that the image triggering should be done, and red, when it should be avoided. Modify the write_to_python.py in order to change the triggering digital channels. The option of removing the button is in the config.py file. If not needed, set the allow_skipping_images to False")
        self.experiment.skip_images = True

    #button to save current sequence as
    self.save_sequence_as_button = QPushButton(self.sequence_tab_widget)
    self.save_sequence_as_button.setFont(QFont('Arial', 14))
    self.save_sequence_as_button.setGeometry(width_of_table + 50, 380, 200, 30)
    self.save_sequence_as_button.setText("Save sequence as")
    self.save_sequence_as_button.clicked.connect(self.save_sequence_as_button_clicked)
    self.save_sequence_as_button.setToolTip("Save sequence as button allows the user to save sequences as a separate files. The currently open file will not be altered.")

    #button to save default
    self.save_default = QPushButton(self.sequence_tab_widget)
    self.save_default.setFont(QFont('Arial', 14))
    self.save_default.setGeometry(width_of_table + 50, 480, 200, 30)
    self.save_default.setText("Save default")
    self.save_default.clicked.connect(self.save_default_button_clicked)
    self.save_default.setToolTip("Save default button allows the user to overwrite the default state which includes the Default edge, corresponding digital, analog, and dds channels values, and channels titles. Once the default is being overwritten, next time the program is initialized with the updated default values. However, when the seqeunce is being loaded it will overwrite accodring to the saved sequence definitions.")

    #button to load default
    self.load_default = QPushButton(self.sequence_tab_widget)
    self.load_default.setFont(QFont('Arial', 14))
    self.load_default.setGeometry(width_of_table + 50, 530, 200, 30)
    self.load_default.setText("Load default")
    self.load_default.clicked.connect(self.load_default_button_clicked)
    self.load_default.setToolTip("Load default button allows the user to enforce the default state on the Default edge, corresponding digital, analog, and dds channels values, and channels titles. It is useful in case some older sequences are loaded and the user wants to quickly update their default edge and title names to the new default values. For example, if there is a sequence for cooling the atoms where a channel A11 was not used at all. Imagine with time the channel A11 started being used as something, for example MOT coils current voltage control. Then the user can load the old sequence, press Load default button and add whatever description was required for the A11.")

    #button to initialize the hardware
    self.init_hardware = QPushButton(self.sequence_tab_widget)
    self.init_hardware.setFont(QFont('Arial', 14))
    self.init_hardware.setGeometry(width_of_table + 50, 580, 200, 30)
    self.init_hardware.setText("Init. hardware")
    self.init_hardware.clicked.connect(self.init_hardware_button_clicked)
    self.init_hardware.setToolTip("Init. hardware button initializes the hardware and sets its state to the default edge values. Check the init_hardware.py file in order to explicitly see what it does. In some cases the user might want to use additional functionality of Artiq that is beyond Quantrol, then the user should modify write_to_python.py go_to_edge function to include the things that require initialization. Same goes to the set_att definitions.")
    
    #button to create the run_experiment.py without running the sequence. An option nice to have in case of troubleshooting
    self.generate_run_experiment_py_button = QPushButton(self.sequence_tab_widget)
    self.generate_run_experiment_py_button.setFont(QFont('Arial', 14))
    self.generate_run_experiment_py_button.setGeometry(width_of_table + 50, 630, 200, 30)
    self.generate_run_experiment_py_button.setText("Generate experiment")
    self.generate_run_experiment_py_button.clicked.connect(self.generate_run_experiment_py_button_clicked)
    self.generate_run_experiment_py_button.setToolTip("Generate experiment button is used to generate the python like description of the experimental sequence that is displayed in the Quantrol. It will generate the run_experiment.py file in the same directory of the source_code.py. It is useful for debugging the experimental sequence descriptions without asking to run it. If something does not work first check if you are asking Artiq to do the correct thing by looking at the generated run_experiment.py.")

    #button to submit the run_experiment.py without updating it with the current experimental description. It is useful in case one needs to hard code something in the sequence and wants to just run it
    self.submit_run_experiment_py_button = QPushButton(self.sequence_tab_widget)
    self.submit_run_experiment_py_button.setFont(QFont('Arial', 14))
    self.submit_run_experiment_py_button.setGeometry(width_of_table + 260, 630, 200, 30)
    self.submit_run_experiment_py_button.setText("Submit experiment")
    self.submit_run_experiment_py_button.clicked.connect(self.submit_run_experiment_py_button_clicked)
    self.submit_run_experiment_py_button.setToolTip("Submit experiment button runs the current state of the run_experiment.py file without updating it with the experimental description shown in the Quantrol. It is useful when the user wants to make manual changes in the experimental sequence and run the updated run_experiment.py. For example, user can generate a two variable scan and then hardcore it to make a 2D scan with different setp sizes. Such run_experiment.py files should be properly named and saved in a separate folder for future use. Otherwise, the run_experiment.py will be overwritten by the Quantrol.")
    
    #dummy button for troubleshooting 
    self.dummy_button = QPushButton(self.sequence_tab_widget)
    self.dummy_button.setFont(QFont('Arial', 14))
    self.dummy_button.setGeometry(width_of_table + 50, 680, 200, 30)
    self.dummy_button.setText("Dummy button")
    self.dummy_button.clicked.connect(self.dummy_button_clicked)
    self.dummy_button.setToolTip("Dummy button is used for the debugging purposes. In the source_code.py there is a dummy_button_clicked fucntion that can be used to print various parameters at different times in order to trace the reason if something is misbehaving. Commented out portions of code are good hints for how the user could use that dummy button for debugging. So in case the debugging is required modify the dummy_button_clicked function in the source_code.py and observe the values of interest in the console of the VS Code.")
        
    #BUTTONS AT THE BOTTOM
    #button to stop continuous run
    self.stop_continuous_run_button_sequence = QPushButton(self.sequence_tab_widget)
    self.stop_continuous_run_button_sequence.setFont(QFont('Arial', 14))
    self.stop_continuous_run_button_sequence.setGeometry(10, 1060, 200, 30)
    self.stop_continuous_run_button_sequence.setText("Stop continuous run")
    self.stop_continuous_run_button_sequence.clicked.connect(self.stop_continuous_run_button_clicked)
    self.stop_continuous_run_button_sequence.setToolTip("Stop continuous run button stops whatever experiment was running before. It generates the init_hardware.py according to the latest default edge values and sets the hardware to that state. Again, it does not only stop continuous run, it stops any experiment and can be used to interrupt whatever was running.")
   
    #button to start continuous run
    self.continuous_run_button_sequence = QPushButton(self.sequence_tab_widget)
    self.continuous_run_button_sequence.setFont(QFont('Arial', 14))
    self.continuous_run_button_sequence.setGeometry(220, 1060, 200, 30)
    self.continuous_run_button_sequence.setText("Continuous run")
    self.continuous_run_button_sequence.clicked.connect(self.continuous_run_button_clicked)
    self.continuous_run_button_sequence.setToolTip("Continuous run button generates the experimental sequence description according to the current state of the Quatnrol as a run_experiment.py file and then runs that experimental sequence indefinitely.")
 
    #run experiment
    self.run_experiment_button_sequence = QPushButton(self.sequence_tab_widget)
    self.run_experiment_button_sequence.setFont(QFont('Arial', 14))
    self.run_experiment_button_sequence.setGeometry(430, 1060, 200, 30)
    self.run_experiment_button_sequence.setText("Run experiment")
    self.run_experiment_button_sequence.clicked.connect(self.run_experiment_button_clicked) 
    self.run_experiment_button_sequence.setToolTip("Run experiment button generates the experimental sequence description accodring to the current state of the Quantrol as a run_experiment.py file and then runs that experimental sequence once.")
    
    #go to edge
    self.go_to_edge_button_sequence = QPushButton(self.sequence_tab_widget)
    self.go_to_edge_button_sequence.setFont(QFont('Arial', 14))
    self.go_to_edge_button_sequence.setGeometry(640, 1060, 200, 30)
    self.go_to_edge_button_sequence.setText("Go to Edge")
    self.go_to_edge_button_sequence.clicked.connect(self.go_to_edge_button_clicked)
    self.go_to_edge_button_sequence.setToolTip("Go to Edge button is used to set the state of the hardware to a specific state at a particular edge. The user first needs to choose the edge to go by right clicking the sequence table on the left")
    
    #TABLE OF SCANNING PARAMETERS
    self.scan_table_parameters = QTableWidget()
    self.scan_table_parameters.setColumnCount(3)
    self.scan_table_parameters.setRowCount(0)
    self.scan_table_parameters.verticalHeader().setVisible(False)
    self.scan_table_parameters.setFont(QFont("Arial", 14))
    self.scan_table_parameters.setHorizontalHeaderLabels(["Variable","Min value", "Max value"])
    self.scan_table_parameters.setColumnWidth(0,250)
    self.scan_table_parameters.setColumnWidth(1,200)
    self.scan_table_parameters.setColumnWidth(2,200)
    self.scan_table_parameters.itemChanged.connect(self.scan_table_changed)
    
    #Add scanned variable button
    self.add_scanned_variable_button = QPushButton()
    self.add_scanned_variable_button.setFont(QFont('Arial', 14))
    self.add_scanned_variable_button.resize(200, 50)
    self.add_scanned_variable_button.setText("Add scanned variable")
    self.add_scanned_variable_button.clicked.connect(self.add_scanned_variable_button_pressed)#this should be modified
    self.add_scanned_variable_button.setToolTip("Add scanned variable button is used to add variables that require scanning. First the user should define the variables in the variblas tab and then add scanned variable and overwrite the name of the variable from None to the name of the variable that needs to be scanned. After that the variable value will be disabled and will display 'scanned'. The value of the scanned variable will be assigned to be the min value in order to allow sorting the time edges.")

    #Delete scanned variable button
    self.delete_scanned_variable_button = QPushButton()
    self.delete_scanned_variable_button.setFont(QFont('Arial', 14))
    self.delete_scanned_variable_button.setText("Delete scanned variable")
    self.delete_scanned_variable_button.clicked.connect(self.delete_scanned_variable_button_pressed)#this should be modified
    self.delete_scanned_variable_button.setToolTip("Delete scanned variable button is used to delete variables from the scanning table and hence disable their scans. The user should first right click the variable that needs to be deleted. The Quantrol will set the values of the deleted scanned variables to the values that were defined before the variable was set to scan.")

    #Step size input
    self.number_of_steps_label = QLabel()
    self.number_of_steps_label.setText("Number of steps")
    self.number_of_steps_input = QLineEdit()
    self.number_of_steps_input.editingFinished.connect(self.number_of_steps_input_changed)
    self.number_of_steps_input.setText("1")

    #warning for the user
    self.warning_about_scan_range = QLabel(self.sequence_tab_widget)
    self.warning_about_scan_range.setFont(QFont('Arial', 14))
    self.warning_about_scan_range.setGeometry(width_of_table + 300, 330, 800, 30)
    self.warning_about_scan_range.setText("Make sure the scan of variables remains withing the allowed values range!!!")

    #Horizontal layout
    hBox = QHBoxLayout()
    temp = QWidget()
    hBox.addWidget(self.add_scanned_variable_button)
    hBox.addWidget(self.delete_scanned_variable_button)     
    hBox.addWidget(self.number_of_steps_label)
    hBox.addWidget(self.number_of_steps_input)
    temp.setLayout(hBox)

    #Scan parameters
    self.scan_table = QGroupBox(self.sequence_tab_widget)
    self.scan_table.setTitle("Scan")
    self.scan_table.setCheckable(True)
    self.scan_table.setChecked(False)
    self.scan_table.setFont(QFont("Arial", 14))
    self.scan_table.move(1100, 30)
    self.scan_table.toggled.connect(self.scan_table_checked)
    vBox = QVBoxLayout()
    self.scan_table.setLayout(vBox)
    vBox.addWidget(temp)
    vBox.addWidget(self.scan_table_parameters)
    self.scan_table.setToolTip("This Scan checkbox is used to enable or disable the variables scan. In case of the scan was unchecked the state of the table will be disabled but the previously set parameters of the scan will remain in place. This allows the user to quickly scan and not scan variables on demand. In order to change the parameters of the scan the user should check the Scan checkbox first. Disables scanning table looks a little faded.")

    #show logger of the program
    self.logger = QPlainTextEdit(self.sequence_tab_widget)
    self.logger.setFont(QFont("Arial", 12))
    self.logger.setGeometry(width_of_table + 50, 790, 1000, 300)
    self.logger.setReadOnly(True)
    self.logger.appendPlainText("Welcome to the %s lab! Hope you enjoy your stay here :)" %config.research_group_name)
    self.logger.appendPlainText("Don't forget to initialize the hardware after the power cycle!!!")
    self.logger.appendPlainText("")
    self.logger.appendPlainText(datetime.now().strftime("%D %H:%M:%S - ") + "Program initialized")
    
    #clear logger button
    self.clear_logger_button = QPushButton(self.sequence_tab_widget)
    self.clear_logger_button.setFont(QFont("Arial", 14))
    self.clear_logger_button.setGeometry(width_of_table + 50, 740, 200, 30)
    self.clear_logger_button.setText("Clear logger")
    self.clear_logger_button.clicked.connect(self.clear_logger_button_clicked)

# DIGITAL TAB
def digital_tab_build(self):
    self.digital_tab_num_cols = config.digital_channels_number + 4    
    self.digital_and_analog_table_column_width = 130
    #DIGITAL TAB WIDGET
    self.digital_tab_widget = QWidget()
    digital_lable = QLabel(self.digital_tab_widget)
    digital_lable.setText("Digital channels")
    digital_lable.setFont(QFont('Arial', 14))
    digital_lable.setGeometry(85, 0, 400, 30)
    
    #DIGITAL TAB LAYOUT
    self.digital_table = QTableWidget(self.digital_tab_widget)
    self.digital_table.setGeometry(QRect(10, 30, 1905, 1020))  
    self.digital_table.setColumnCount(self.digital_tab_num_cols)
    self.digital_table.setRowCount(1) 
    self.digital_table.setHorizontalHeaderLabels(self.experiment.title_digital_tab)
    self.digital_table.verticalHeader().setVisible(False)
    self.digital_table.horizontalHeader().setFixedHeight(60)
    self.digital_table.horizontalHeader().setFont(QFont('Arial', 12))
    self.digital_table.setFont(QFont('Arial', 12))
    self.digital_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.digital_table.horizontalHeader().setMinimumSectionSize(0)
    self.digital_table.setColumnWidth(0,50)
    self.digital_table.setColumnWidth(1,180)
    self.digital_table.setColumnWidth(2,100)
    self.digital_table.setColumnWidth(3,5)
    self.digital_table.setFrameStyle(QFrame.NoFrame)
    delegate = ReadOnlyDelegate(self)
    for _ in range(4):
        exec("self.digital_table.setItemDelegateForColumn(%d,delegate)" %_)
    #self.digital_table.setItemDelegateForRow(0, delegate)
    for i in range(4, self.digital_tab_num_cols):
        exec("self.digital_table.setColumnWidth(%d,%d)" % (i, self.digital_and_analog_table_column_width))
    #Filling the DIGITAL table
    for index, channel in enumerate(self.experiment.sequence[0].digital):
        col = index + 4
        self.digital_table.setItem(0, col, QTableWidgetItem(channel.expression))
        if channel.value == 1:
            self.digital_table.item(0, col).setBackground(self.green)
        else:
            self.digital_table.item(0, col).setBackground(self.red)
    #Binding functions
    self.digital_table.itemChanged.connect(self.digital_table_changed)
    self.digital_table.horizontalHeader().sectionClicked.connect(self.digital_table_header_clicked)



    #Dummy table that will display edge number, name and time and will be fixed
    self.digital_dummy = QTableWidget(self.digital_tab_widget)
    self.digital_dummy.setGeometry(QRect(10, 30, 330, 1003))
    self.digital_dummy.setColumnCount(3)
    self.digital_dummy.setRowCount(1)
    self.digital_dummy.setHorizontalHeaderLabels(self.experiment.title_digital_tab[0:3])
    self.digital_dummy.verticalHeader().setVisible(False)
    self.digital_dummy.horizontalHeader().setFixedHeight(60)
    self.digital_dummy.horizontalHeader().setFont(QFont('Arial', 12))
    self.digital_dummy.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.digital_dummy.setFont(QFont('Arial', 12))
    self.digital_dummy.setColumnWidth(0,50)
    self.digital_dummy.setColumnWidth(1,180)
    self.digital_dummy.setColumnWidth(2,100)
    self.digital_dummy.setFrameStyle(QFrame.NoFrame)
    #Setting the left part of the DIGITAL table (edge number, name, time)
    self.digital_dummy.setItem(0, 0, QTableWidgetItem("0"))
    self.digital_dummy.setItem(0, 1, QTableWidgetItem(self.experiment.sequence[0].name))
    self.digital_dummy.setItem(0, 2, QTableWidgetItem(str(self.experiment.sequence[0].value)))
    delegate = ReadOnlyDelegate(self)
    for _ in range(3):
        exec("self.digital_dummy.setItemDelegateForColumn(%d,delegate)" %_)
        
    self.digital_dummy.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.digital_dummy.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    #BUTTONS AT THE BOTTOM
    #button to stop continuous run
    self.stop_continuous_run_button_digital = QPushButton(self.digital_tab_widget)
    self.stop_continuous_run_button_digital.setFont(QFont('Arial', 14))
    self.stop_continuous_run_button_digital.setGeometry(10, 1060, 200, 30)
    self.stop_continuous_run_button_digital.setText("Stop continuous run")
    self.stop_continuous_run_button_digital.clicked.connect(self.stop_continuous_run_button_clicked)
    self.stop_continuous_run_button_digital.setToolTip("Stop continuous run button stops whatever experiment was running before. It generates the init_hardware.py according to the latest default edge values and sets the hardware to that state. Again, it does not only stop continuous run, it stops any experiment and can be used to interrupt whatever was running.")
   
    #button to start continuous run
    self.continuous_run_button_digital = QPushButton(self.digital_tab_widget)
    self.continuous_run_button_digital.setFont(QFont('Arial', 14))
    self.continuous_run_button_digital.setGeometry(220, 1060, 200, 30)
    self.continuous_run_button_digital.setText("Continuous run")
    self.continuous_run_button_digital.clicked.connect(self.continuous_run_button_clicked)
    self.continuous_run_button_digital.setToolTip("Continuous run button generates the experimental sequence description according to the current state of the Quatnrol as a run_experiment.py file and then runs that experimental sequence indefinitely.")
    
 
    #run experiment
    self.run_experiment_button_digital = QPushButton(self.digital_tab_widget)
    self.run_experiment_button_digital.setFont(QFont('Arial', 14))
    self.run_experiment_button_digital.setGeometry(430, 1060, 200, 30)
    self.run_experiment_button_digital.setText("Run experiment")
    self.run_experiment_button_digital.clicked.connect(self.run_experiment_button_clicked) 
    self.run_experiment_button_digital.setToolTip("Run experiment button generates the experimental sequence description accodring to the current state of the Quantrol as a run_experiment.py file and then runs that experimental sequence once.")
    
    #go to edge
    self.go_to_edge_button_digital = QPushButton(self.digital_tab_widget)
    self.go_to_edge_button_digital.setFont(QFont('Arial', 14))
    self.go_to_edge_button_digital.setGeometry(640, 1060, 200, 30)
    self.go_to_edge_button_digital.setText("Go to Edge")
    self.go_to_edge_button_digital.clicked.connect(self.go_to_edge_button_clicked)
    self.go_to_edge_button_digital.setToolTip("Go to Edge button is used to set the state of the hardware to a specific state at a particular edge. The user first needs to choose the edge to go by right clicking the sequence table on the left")


#ANALOG TAB
def analog_tab_build(self):
    self.analog_tab_num_cols = config.analog_channels_number + 4    
    #ANALOG TAB WIDGET
    self.analog_tab_widget = QWidget()
    #ANALOG LABLE
    analog_lable = QLabel(self.analog_tab_widget)
    analog_lable.setText("Analog channels")
    analog_lable.setFont(QFont('Arial', 14))
    analog_lable.setGeometry(85, 0, 400, 30)


    #ANALOG TAB LAYOUT
    self.analog_table = QTableWidget(self.analog_tab_widget)
    self.analog_table.setGeometry(QRect(10, 30, 1905, 1020))  
    self.analog_table.setColumnCount(self.analog_tab_num_cols) 
    self.analog_table.setRowCount(1)
    self.analog_table.setHorizontalHeaderLabels(self.experiment.title_analog_tab)
    self.analog_table.verticalHeader().setVisible(False)
    self.analog_table.horizontalHeader().setFixedHeight(60)
    self.analog_table.horizontalHeader().setFont(QFont('Arial', 12))
    self.analog_table.setFont(QFont('Arial', 12))
    self.analog_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.analog_table.horizontalHeader().setMinimumSectionSize(0)
    self.analog_table.setColumnWidth(0,50)
    self.analog_table.setColumnWidth(1,180)
    self.analog_table.setColumnWidth(2,100)
    self.analog_table.setColumnWidth(3,5)
    self.analog_table.setFrameStyle(QFrame.NoFrame)
    delegate = ReadOnlyDelegate(self)
    for _ in range(4):
        exec("self.analog_table.setItemDelegateForColumn(%d,delegate)" %_)
    #self.analog_table.setItemDelegateForRow(0,delegate)
    for i in range(4, self.analog_tab_num_cols):
        exec("self.analog_table.setColumnWidth(%d,%d)" % (i,self.digital_and_analog_table_column_width))
    #Filling the default values
    for index, channel in enumerate(self.experiment.sequence[0].analog):
        # plus 3 is because first 3 columns are used by number, name and time of edge
        col = index + 4
        self.analog_table.setItem(0, col, QTableWidgetItem(channel.expression))
        self.analog_table.item(0, col).setToolTip(str(channel.value))
        if channel.value != 0:
            self.analog_table.item(0, col).setBackground(self.green)
        else:
            self.analog_table.item(0, col).setBackground(self.red)
    
    self.analog_table.itemChanged.connect(self.analog_table_changed)
    self.analog_table.horizontalHeader().sectionClicked.connect(self.analog_table_header_clicked)

    #Dummy table that will display edge number, name and time and will be fixed
    self.analog_dummy = QTableWidget(self.analog_tab_widget)
    self.analog_dummy.setGeometry(QRect(10, 30, 330, 1003))
    self.analog_dummy.setColumnCount(3)
    self.analog_dummy.setRowCount(1)
    self.analog_dummy.setHorizontalHeaderLabels(self.experiment.title_analog_tab[0:3])
    self.analog_dummy.verticalHeader().setVisible(False)
    self.analog_dummy.horizontalHeader().setFixedHeight(60)
    self.analog_dummy.horizontalHeader().setFont(QFont('Arial', 12))
    self.analog_dummy.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.analog_dummy.setFont(QFont('Arial', 12))
    self.analog_dummy.setColumnWidth(0,50)
    self.analog_dummy.setColumnWidth(1,180)
    self.analog_dummy.setColumnWidth(2,100)
    self.analog_dummy.setFrameStyle(QFrame.NoFrame)
    #Setting the left part of the analog table
    self.analog_dummy.setItem(0, 0, QTableWidgetItem("0"))
    self.analog_dummy.setItem(0, 1, QTableWidgetItem(self.experiment.sequence[0].name))
    self.analog_dummy.setItem(0, 2, QTableWidgetItem(str(self.experiment.sequence[0].value)))    

    delegate = ReadOnlyDelegate(self)
    for _ in range(3):
        exec("self.analog_dummy.setItemDelegateForColumn(%d,delegate)" %_)

    self.analog_dummy.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.analog_dummy.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    #BUTTONS AT THE BOTTOM
    #button to stop continuous run
    self.stop_continuous_run_button_analog = QPushButton(self.analog_tab_widget)
    self.stop_continuous_run_button_analog.setFont(QFont('Arial', 14))
    self.stop_continuous_run_button_analog.setGeometry(10, 1060, 200, 30)
    self.stop_continuous_run_button_analog.setText("Stop continuous run")
    self.stop_continuous_run_button_analog.clicked.connect(self.stop_continuous_run_button_clicked)
    self.stop_continuous_run_button_analog.setToolTip("Stop continuous run button stops whatever experiment was running before. It generates the init_hardware.py according to the latest default edge values and sets the hardware to that state. Again, it does not only stop continuous run, it stops any experiment and can be used to interrupt whatever was running.")
   
    #button to start continuous run
    self.continuous_run_button_analog = QPushButton(self.analog_tab_widget)
    self.continuous_run_button_analog.setFont(QFont('Arial', 14))
    self.continuous_run_button_analog.setGeometry(220, 1060, 200, 30)
    self.continuous_run_button_analog.setText("Continuous run")
    self.continuous_run_button_analog.clicked.connect(self.continuous_run_button_clicked)
    self.continuous_run_button_analog.setToolTip("Continuous run button generates the experimental sequence description according to the current state of the Quatnrol as a run_experiment.py file and then runs that experimental sequence indefinitely.")
 
    #run experiment
    self.run_experiment_button_analog = QPushButton(self.analog_tab_widget)
    self.run_experiment_button_analog.setFont(QFont('Arial', 14))
    self.run_experiment_button_analog.setGeometry(430, 1060, 200, 30)
    self.run_experiment_button_analog.setText("Run experiment")
    self.run_experiment_button_analog.clicked.connect(self.run_experiment_button_clicked) 
    self.run_experiment_button_analog.setToolTip("Run experiment button generates the experimental sequence description accodring to the current state of the Quantrol as a run_experiment.py file and then runs that experimental sequence once.")
    
    #go to edge
    self.go_to_edge_button_analog = QPushButton(self.analog_tab_widget)
    self.go_to_edge_button_analog.setFont(QFont('Arial', 14))
    self.go_to_edge_button_analog.setGeometry(640, 1060, 200, 30)
    self.go_to_edge_button_analog.setText("Go to Edge")
    self.go_to_edge_button_analog.clicked.connect(self.go_to_edge_button_clicked)
    self.go_to_edge_button_analog.setToolTip("Go to Edge button is used to set the state of the hardware to a specific state at a particular edge. The user first needs to choose the edge to go by right clicking the sequence table on the left")


def dds_tab_build(self):
    self.dds_tab_num_cols = 6*config.dds_channels_number + 3
    #DDS TABLE WIDGET
    self.dds_tab_widget = QWidget()
    #DDS LABLE
    dds_lable = QLabel(self.dds_tab_widget)
    dds_lable.setText("Dds channels")
    dds_lable.setFont(QFont('Arial', 14))
    dds_lable.setGeometry(85, 0, 400, 30)
    self.sequence_num_rows = len(self.experiment.sequence)
    
    #DDS TAB LAYOUT
    self.dds_table = QTableWidget(self.dds_tab_widget)
    self.dds_table.setGeometry(QRect(10, 30, 1905, 1020))
    self.dds_table.setColumnCount(self.dds_tab_num_cols)
    self.dds_table.horizontalHeader().setMinimumHeight(50)
    self.dds_table.verticalHeader().setVisible(False)
    self.dds_table.horizontalHeader().setVisible(False)
    self.dds_table.setRowCount(3) # 5 is an arbitrary number we just need to have rows in order to span them
    self.dds_table.horizontalHeader().setMinimumSectionSize(0)
    self.dds_table.setFont(QFont('Arial', 12))
    self.dds_table.setFrameStyle(QFrame.NoFrame)
    #SHAPING THE FIRST 3 COLUMNS 
    self.dds_table.setColumnWidth(0,50)
    self.dds_table.setColumnWidth(1,180)
    self.dds_table.setColumnWidth(2,100)
    self.dds_table.setColumnWidth(3,5)

    delegate = ReadOnlyDelegate(self)
    #SHAPING THE TABLE
    for i in range(config.dds_channels_number):
        self.dds_table.setSpan(0,4 + 6*i, 1, 5) # stretching the title of the channel
        self.dds_table.setColumnWidth(3 + 6*i, 5) # making separation line thin
        self.dds_table.setColumnWidth(8 + 6*i, 45) # making state column smaller
        self.dds_table.setItemDelegateForColumn(3 + 6*i,delegate) #making separation line uneditable
    
    #making first three columns verticaly wider to fit with header 
    for i in range(3):
        self.dds_table.setSpan(0, i, 2, 1)
        self.dds_table.setItemDelegateForColumn(i,delegate)
    #Filling the default values of DDS table
    for index, channel in enumerate(self.experiment.sequence[0].dds):
        #plus 4 is because first 4 columns are used by number, name, time and separator(dark grey line)
        col = 4 + index * 6  
        for setting in range(5):
            exec("self.dds_table.setItem(2, col + setting, QTableWidgetItem(str(channel.%s.expression)))" %self.setting_dict[setting])
            exec("self.dds_table.item(2, col + setting).setToolTip(str(channel.%s.value))" %self.setting_dict[setting])
            if channel.state.value == 1:
                self.dds_table.item(2, col + setting).setBackground(self.green)
            else:  
                self.dds_table.item(2, col + setting).setBackground(self.red)


    self.dds_table.itemChanged.connect(self.dds_table_changed)

    #Dummy table that will display edge number, name and time and will be fixed (LEFT SIDE OF THE TABLE)
    self.dds_dummy = QTableWidget(self.dds_tab_widget)
    self.dds_dummy.setGeometry(QRect(10,30,335,1003))
    self.dds_dummy.setColumnCount(4)
    self.dds_dummy.setRowCount(3)
    self.dds_dummy.horizontalHeader().setMinimumHeight(50)
    self.dds_dummy.verticalHeader().setVisible(False)
    self.dds_dummy.horizontalHeader().setVisible(False)
    self.dds_dummy.horizontalHeader().setMinimumSectionSize(0)
    self.dds_dummy.horizontalHeader().setFont(QFont('Arial', 12))
    self.dds_dummy.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.dds_dummy.setFont(QFont('Arial', 12))
    self.dds_dummy.setColumnWidth(0,50)
    self.dds_dummy.setColumnWidth(1,180)
    self.dds_dummy.setColumnWidth(2,100)
    self.dds_dummy.setColumnWidth(3,5)
    self.dds_dummy.setFrameStyle(QFrame.NoFrame)

    #making first three columns vertically wider to fit with header 
    for i in range(3):
        self.dds_dummy.setSpan(0, i, 2, 1)
        self.dds_dummy.setItemDelegateForColumn(i,delegate)
    #Filling the left part of the DDS table
    self.dds_dummy.setItem(2, 0, QTableWidgetItem("0"))
    self.dds_dummy.setItem(2, 1, QTableWidgetItem(self.experiment.sequence[0].name))
    self.dds_dummy.setItem(2, 2, QTableWidgetItem(str(self.experiment.sequence[0].value)))


    #Dummy horizontal header (TOP SIDE OF THE TABLE)
    self.dds_dummy_header = QTableWidget(self.dds_tab_widget)
    self.dds_dummy_header.setGeometry(QRect(10,30,1905,60))
    self.dds_dummy_header.setColumnCount(self.dds_tab_num_cols)
    self.dds_dummy_header.horizontalHeader().setMinimumHeight(50)
    self.dds_dummy_header.verticalHeader().setVisible(False)
    self.dds_dummy_header.horizontalHeader().setVisible(False)
    self.dds_dummy_header.setRowCount(2) 
    self.dds_dummy_header.horizontalHeader().setMinimumSectionSize(0)
    self.dds_dummy_header.horizontalHeader().setFont(QFont('Arial', 12))
    self.dds_dummy_header.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.dds_dummy_header.setFont(QFont('Arial', 12))
    self.dds_dummy_header.setFrameStyle(QFrame.NoFrame)
    #SHAPING THE FIRST 3 COLUMNS 
    self.dds_dummy_header.setColumnWidth(0,50) 
    self.dds_dummy_header.setColumnWidth(1,180)
    self.dds_dummy_header.setColumnWidth(2,100)

    #SHAPING THE TABLE
    for i in range(config.dds_channels_number):
        self.dds_dummy_header.setSpan(0,4 + 6*i, 1, 5) # stretching the title of the channel
        self.dds_dummy_header.setColumnWidth(3 + 6*i, 5) # making separation line thin
        self.dds_dummy_header.setColumnWidth(8 + 6*i, 45) # making state column smaller
        self.dds_dummy_header.setItemDelegateForColumn(3 + 6*i,delegate) #making separation line uneditable

    self.dds_dummy_header.setItemDelegateForRow(1, delegate) #making row number 2 uneditable

    #populating headers and separators
    for i in range(config.dds_channels_number):
        #separator
        self.dds_dummy_header.setSpan(0, 6*i + 3, self.sequence_num_rows+2, 1)
        self.dds_dummy_header.setItem(0,6*i + 3, QTableWidgetItem())
        self.dds_dummy_header.item(0, 6*i + 3).setBackground(self.grey)
        #headers Channel
        self.dds_dummy_header.setItem(0,6*i+4, QTableWidgetItem(str(self.experiment.title_dds_tab[i+4])))
        self.dds_dummy_header.item(0,6*i+4).setTextAlignment(Qt.AlignCenter)
        #headers Channel attributes (f, Amp, att, phase, state)
        self.dds_dummy_header.setItem(1,6*i+4, QTableWidgetItem('f (MHz)'))
        self.dds_dummy_header.setItem(1,6*i+5, QTableWidgetItem('Amp (dBm)'))
        self.dds_dummy_header.setItem(1,6*i+6, QTableWidgetItem('Att (dBm)'))
        self.dds_dummy_header.setItem(1,6*i+7, QTableWidgetItem('phase (deg)'))
        self.dds_dummy_header.setItem(1,6*i+8, QTableWidgetItem('state'))

    self.dds_dummy_header.itemChanged.connect(self.dds_dummy_header_changed)

    #Making fixed corner (TOP LEFT SIDE OF THE TABLE)
    self.dds_fixed = QTableWidget(self.dds_tab_widget)
    self.dds_fixed.setGeometry(QRect(10,30, 335,60))
    self.dds_fixed.setColumnCount(4)
    self.dds_fixed.horizontalHeader().setMinimumHeight(50)
    self.dds_fixed.verticalHeader().setVisible(False)
    self.dds_fixed.horizontalHeader().setVisible(False)
    self.dds_fixed.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.dds_fixed.horizontalHeader().setMinimumSectionSize(0)
    self.dds_fixed.setRowCount(2) 
    self.dds_fixed.setFont(QFont('Arial', 12))
    self.dds_fixed.setFrameStyle(QFrame.NoFrame)
    #SHAPING THE FIRST 3 COLUMNS
    self.dds_fixed.setColumnWidth(0,50)
    self.dds_fixed.setColumnWidth(1,180)
    self.dds_fixed.setColumnWidth(2,100)
    self.dds_fixed.setColumnWidth(3,5)
    #making first three columns vertically wider to fit with header 
    for i in range(4):
        self.dds_fixed.setSpan(0, i, 2, 1)
        self.dds_fixed.setItemDelegateForColumn(i,delegate)
    #Separator
    self.dds_fixed.setItem(0,3, QTableWidgetItem())
    self.dds_fixed.item(0,3).setBackground(self.grey)
    #populating edge number, name and time
    for i in range(3):
        self.dds_fixed.setItem(0,i, QTableWidgetItem(str(self.experiment.title_dds_tab[i])))
        self.dds_fixed.item(0,i).setTextAlignment(Qt.AlignCenter)

    #MAKING VERTICAL SCROLL BARS COMMON FOR DDS TABLE
    self.dds_tables = [self.dds_table,self.dds_dummy,self.analog_table,self.analog_dummy, self.digital_table, self.digital_dummy, self.sequence_table]

    def move_other_scrollbars_vertical(idx,bar):
        scrollbars = {tbl.verticalScrollBar() for tbl in self.dds_tables}
        scrollbars.remove(bar)
        for bar in scrollbars:
            bar.setValue(idx)
        
    self.dds_dummy.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.dds_dummy.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    for tbl in self.dds_tables:
        scrollbar = tbl.verticalScrollBar()
        scrollbar.valueChanged.connect(lambda idx,bar=scrollbar: move_other_scrollbars_vertical(idx, bar))

    #MAKING HORIZONTAL SCROLL BARS COMMON FOR DDS TABLE
    self.dds_dummy_tables = [self.dds_table,self.dds_dummy_header]

    def move_other_scrollbars_horizontal(idx,bar):
        scrollbars = {tbl.horizontalScrollBar() for tbl in self.dds_dummy_tables}
        scrollbars.remove(bar)
        for bar in scrollbars:
            bar.setValue(idx)
        
    self.dds_dummy_header.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.dds_dummy_header.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    for tbl in self.dds_dummy_tables:
        scrollbar = tbl.horizontalScrollBar()
        scrollbar.valueChanged.connect(lambda idx,bar=scrollbar: move_other_scrollbars_horizontal(idx, bar))

    
    #BUTTONS AT THE BOTTOM
    #button to stop continuous run
    self.stop_continuous_run_button_dds = QPushButton(self.dds_tab_widget)
    self.stop_continuous_run_button_dds.setFont(QFont('Arial', 14))
    self.stop_continuous_run_button_dds.setGeometry(10, 1060, 200, 30)
    self.stop_continuous_run_button_dds.setText("Stop continuous run")
    self.stop_continuous_run_button_dds.clicked.connect(self.stop_continuous_run_button_clicked)
    self.stop_continuous_run_button_dds.setToolTip("Stop continuous run button stops whatever experiment was running before. It generates the init_hardware.py according to the latest default edge values and sets the hardware to that state. Again, it does not only stop continuous run, it stops any experiment and can be used to interrupt whatever was running.")
   
    #button to start continuous run
    self.continuous_run_button_dds = QPushButton(self.dds_tab_widget)
    self.continuous_run_button_dds.setFont(QFont('Arial', 14))
    self.continuous_run_button_dds.setGeometry(220, 1060, 200, 30)
    self.continuous_run_button_dds.setText("Continuous run")
    self.continuous_run_button_dds.clicked.connect(self.continuous_run_button_clicked)
    self.continuous_run_button_dds.setToolTip("Continuous run button generates the experimental sequence description according to the current state of the Quatnrol as a run_experiment.py file and then runs that experimental sequence indefinitely.")
 
    #run experiment
    self.run_experiment_button_dds = QPushButton(self.dds_tab_widget)
    self.run_experiment_button_dds.setFont(QFont('Arial', 14))
    self.run_experiment_button_dds.setGeometry(430, 1060, 200, 30)
    self.run_experiment_button_dds.setText("Run experiment")
    self.run_experiment_button_dds.clicked.connect(self.run_experiment_button_clicked) 
    self.run_experiment_button_dds.setToolTip("Run experiment button generates the experimental sequence description accodring to the current state of the Quantrol as a run_experiment.py file and then runs that experimental sequence once.")
    
    #go to edge
    self.go_to_edge_button_dds = QPushButton(self.dds_tab_widget)
    self.go_to_edge_button_dds.setFont(QFont('Arial', 14))
    self.go_to_edge_button_dds.setGeometry(640, 1060, 200, 30)
    self.go_to_edge_button_dds.setText("Go to Edge")
    self.go_to_edge_button_dds.clicked.connect(self.go_to_edge_button_clicked)
    self.go_to_edge_button_dds.setToolTip("Go to Edge button is used to set the state of the hardware to a specific state at a particular edge. The user first needs to choose the edge to go by right clicking the sequence table on the left")


def variables_tab_build(self):
    #VARIABLES TAB WIDGET
    self.variables_tab_widget = QWidget()
    #VARIABLES LABLE
    variables_lable = QLabel(self.variables_tab_widget)
    variables_lable.setText("Constant variables")
    variables_lable.setFont(QFont('Arial', 14))
    variables_lable.setGeometry(85, 0, 400, 30)

    #VARIABLES TABLE LAYOUT
    self.variables_table = QTableWidget(self.variables_tab_widget)
    width_of_table_variables = 410
    self.variables_table.setGeometry(QRect(10, 30, width_of_table_variables, 1010))                                                #size of the table
    variables_num_columns = 2 #2 for proof of concept
    self.variables_table.setColumnCount(variables_num_columns)
    self.variables_table.setHorizontalHeaderLabels(["Name", "Value"])
    self.variables_table.verticalHeader().setVisible(False)
    self.variables_table.horizontalHeader().setFixedHeight(50)
    self.variables_table.horizontalHeader().setFont(QFont('Arial', 12))
    self.variables_table.setFont(QFont('Arial', 12))
    self.variables_table.setColumnWidth(0,205)
    self.variables_table.setColumnWidth(1,203)
    #when table contents are changed
    self.variables_table.itemChanged.connect(self.variables_table_changed)
    #button to create new variable
    self.create_new_variable = QPushButton(self.variables_tab_widget)
    self.create_new_variable.setFont(QFont('Arial', 14))
    self.create_new_variable.setGeometry(10, 1050, 200, 30)
    self.create_new_variable.setText("Create new variable")
    self.create_new_variable.setToolTip("Button that is used to create a new variable.")
    self.create_new_variable.clicked.connect(self.create_new_variable_button_clicked)
    #button to delete a variable
    self.delete_variable = QPushButton(self.variables_tab_widget)
    self.delete_variable.setFont(QFont('Arial', 14))
    self.delete_variable.setGeometry(220, 1050, 200, 30)
    self.delete_variable.setText("Delete variable")
    self.delete_variable.setToolTip("Button that is used to delete a new variable. First choose the new varibles by right clicking it in the variables table.")
    self.delete_variable.clicked.connect(self.delete_variable_button_clicked)
    
    #DERIVED VARIABLES LABLE
    derived_variables_lable = QLabel(self.variables_tab_widget)
    derived_variables_lable.setText("Derived variables")
    derived_variables_lable.setFont(QFont('Arial', 14))
    derived_variables_lable.setGeometry(515, 0, 400, 30)

    #DERIVED VARIABLES TABLE LAYOUT
    self.derived_variables_table = QTableWidget(self.variables_tab_widget)
    width_of_table_variables = 420
    self.derived_variables_table.setGeometry(QRect(440, 30, 700, 1010))  #size of the table
    derived_variables_num_columns = 4 
    self.derived_variables_table.setColumnCount(derived_variables_num_columns)
    self.derived_variables_table.setHorizontalHeaderLabels(["Name", "Arguments", "Edge id","Function in python syntax"])
    self.derived_variables_table.verticalHeader().setVisible(False)
    self.derived_variables_table.horizontalHeader().setFixedHeight(50)
    self.derived_variables_table.horizontalHeader().setFont(QFont('Arial', 12))
    self.derived_variables_table.setFont(QFont('Arial', 12))
    self.derived_variables_table.setColumnWidth(0,130)
    self.derived_variables_table.setColumnWidth(1,100)
    self.derived_variables_table.setColumnWidth(2,70)
    self.derived_variables_table.setColumnWidth(3,398)
    self.derived_variables_table.setRowCount(1)
    prototypeItem = QTableWidgetItem()
    prototypeItem.setTextAlignment(Qt.AlignCenter)
    self.derived_variables_table.setItemPrototype(prototypeItem)
    #Disabling the first example row
    delegate = ReadOnlyDelegate(self)
    self.derived_variables_table.setItemDelegateForRow(0,delegate)
    self.derived_variables_table.setItem(0, 0, QTableWidgetItem("example_name"))
    self.derived_variables_table.item(0,0).setToolTip("Name of the derived variable")
    self.derived_variables_table.setItem(0, 1, QTableWidgetItem("x,y"))
    self.derived_variables_table.item(0,1).setToolTip("Comma separated arguments of the function to be used to derive the variable")
    self.derived_variables_table.setItem(0, 2, QTableWidgetItem("id5"))
    self.derived_variables_table.item(0,2).setToolTip("ID of the edge when user wants to request the calculation of the derived variable")
    self.derived_variables_table.setItem(0, 3, QTableWidgetItem("np.sin(x) + 5*np.sqrt(y)"))
    self.derived_variables_table.item(0,1).setToolTip("Function to be used to derive the variable. It should be python compatible with the numpy being imported as np")
    #when table contents are changed
    self.derived_variables_table.itemChanged.connect(self.derived_variables_table_changed)

    #button to create new derived variable
    self.create_derived_variable = QPushButton(self.variables_tab_widget)
    self.create_derived_variable.setFont(QFont('Arial', 14))
    self.create_derived_variable.setGeometry(440, 1050, 200, 30)
    self.create_derived_variable.setText("Create derived variable")
    self.create_derived_variable.setToolTip("Button that is used to create a new derived variable. Please input arguments and edge id before using the variable")
    self.create_derived_variable.clicked.connect(self.create_derived_variable_button_clicked)
    #button to delete a variable
    self.delete_derived_variable = QPushButton(self.variables_tab_widget)
    self.delete_derived_variable.setFont(QFont('Arial', 14))
    self.delete_derived_variable.setGeometry(650, 1050, 200, 30)
    self.delete_derived_variable.setText("Delete derived variable")
    self.delete_derived_variable.setToolTip("Button that is used to delete a derived variable. First choose the derived variable by right clicking it in the derived variables table.")
    self.delete_derived_variable.clicked.connect(self.delete_derived_variable_button_clicked)

    #LOOKUP VARIABLES LABLE
    lookup_variables_lable = QLabel(self.variables_tab_widget)
    lookup_variables_lable.setText("Lookup variables")
    lookup_variables_lable.setFont(QFont('Arial', 14))
    lookup_variables_lable.setGeometry(1235, 0, 500, 30)

    #LOOKUP VARIABLES TABLE LAYOUT
    self.lookup_variables_table = QTableWidget(self.variables_tab_widget)
    width_of_table_variables = 420
    self.lookup_variables_table.setGeometry(QRect(1160, 30, 745, 1010))  #size of the table
    lookup_variables_num_columns = 3
    self.lookup_variables_table.setColumnCount(lookup_variables_num_columns)
    self.lookup_variables_table.setHorizontalHeaderLabels(["Name", "Agrument", "Lookup list name"])
    self.lookup_variables_table.verticalHeader().setVisible(False)
    self.lookup_variables_table.horizontalHeader().setFixedHeight(50)
    self.lookup_variables_table.horizontalHeader().setFont(QFont('Arial', 12))
    self.lookup_variables_table.setFont(QFont('Arial', 12))
    self.lookup_variables_table.setColumnWidth(0,180)
    self.lookup_variables_table.setColumnWidth(1,150)
    self.lookup_variables_table.setColumnWidth(2,413)
    self.lookup_variables_table.setRowCount(1)
    prototypeItem = QTableWidgetItem()
    prototypeItem.setTextAlignment(Qt.AlignCenter)
    self.lookup_variables_table.setItemPrototype(prototypeItem)
    #Disabling the first example row
    delegate = ReadOnlyDelegate(self)
    self.lookup_variables_table.setItemDelegateForRow(0,delegate)
    self.lookup_variables_table.setItemDelegateForColumn(2,delegate)
    self.lookup_variables_table.setItem(0, 0, QTableWidgetItem("example_name"))
    self.lookup_variables_table.item(0,0).setToolTip("Name of the lookup variable")
    self.lookup_variables_table.setItem(0, 1, QTableWidgetItem("sampled_var"))
    self.lookup_variables_table.item(0,1).setToolTip("Name of the sampled variable that is going to be used as an argument for the lookup list")
    self.lookup_variables_table.setItem(0, 2, QTableWidgetItem("gaussian_fit"))
    self.lookup_variables_table.item(0,0).setToolTip("Name of the lookup list to remind the user the purpose of the lookup variable")
    #when table contents are changed
    self.lookup_variables_table.itemChanged.connect(self.lookup_variables_table_changed)

    #button to create new lookup variable
    self.create_lookup_variable = QPushButton(self.variables_tab_widget)
    self.create_lookup_variable.setFont(QFont('Arial', 14))
    self.create_lookup_variable.setGeometry(1160, 1050, 200, 30)
    self.create_lookup_variable.setText("Create lookup variable")
    self.create_lookup_variable.setToolTip("Button that is used to create a new lookup variable. Please input the arguments before using the variable")
    self.create_lookup_variable.clicked.connect(self.create_lookup_variable_button_clicked)
    #button to delete a variable
    self.delete_lookup_variable = QPushButton(self.variables_tab_widget)
    self.delete_lookup_variable.setFont(QFont('Arial', 14))
    self.delete_lookup_variable.setGeometry(1370, 1050, 200, 30)
    self.delete_lookup_variable.setText("Delete lookup variable")
    self.delete_lookup_variable.setToolTip("Button that is used to delete a lookup variable. First choose the lookup variable by right clikcing it in the lookup variables table.")
    self.delete_lookup_variable.clicked.connect(self.delete_lookup_variable_button_clicked)
    #button to load the lookup table
    self.load_lookup_list = QPushButton(self.variables_tab_widget)
    self.load_lookup_list.setFont(QFont('Arial', 14))
    self.load_lookup_list.setGeometry(1580, 1050, 200, 30)
    self.load_lookup_list.setText("Load lookup list")
    self.load_lookup_list.setToolTip("Button is used to load the lookup list for the variable. First choose the lookup variable by right clicking it in the lookup variables table. After that navigate and open the lookup variable list. It should be of the .mat format.")
    self.load_lookup_list.clicked.connect(self.load_lookup_list_button_clicked)
        
# SAMPLER TAB
def sampler_tab_build(self):
    self.sampler_tab_num_cols = config.sampler_channels_number + 4    
    self.sampler_table_column_width = 196
    #SAMPLER TAB WIDGET
    self.sampler_tab_widget = QWidget()
    sampler_lable = QLabel(self.sampler_tab_widget)
    sampler_lable.setText("Sampler channels")
    sampler_lable.setFont(QFont('Arial', 14))
    sampler_lable.setGeometry(85, 0, 400, 30)
    
    #SAMPLER TAB LAYOUT
    self.sampler_table = QTableWidget(self.sampler_tab_widget)
    self.sampler_table.setGeometry(QRect(10, 30, 1905, 1020))  
    self.sampler_table.setColumnCount(self.sampler_tab_num_cols)
    self.sampler_table.setRowCount(1) 
    self.sampler_table.setHorizontalHeaderLabels(self.experiment.title_sampler_tab)
    self.sampler_table.verticalHeader().setVisible(False)
    self.sampler_table.horizontalHeader().setFixedHeight(60)
    self.sampler_table.horizontalHeader().setFont(QFont('Arial', 12))
    self.sampler_table.setFont(QFont('Arial', 12))
    self.sampler_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.sampler_table.horizontalHeader().setMinimumSectionSize(0)
    self.sampler_table.setColumnWidth(0,50)
    self.sampler_table.setColumnWidth(1,180)
    self.sampler_table.setColumnWidth(2,100)
    self.sampler_table.setColumnWidth(3,5)
    self.sampler_table.setFrameStyle(QFrame.NoFrame)
    for i in range(4, self.sampler_tab_num_cols):
        exec("self.sampler_table.setColumnWidth(%d,%d)" % (i, self.sampler_table_column_width))

    for index, channel in enumerate(self.experiment.sequence[0].sampler):
        col = index + 4
        self.sampler_table.setItem(0, col, QTableWidgetItem(str(channel)))
        if channel != "0":
            self.sampler_table.item(0, col).setBackground(self.green)
        else:
            self.sampler_table.item(0, col).setBackground(self.white)
    #Binding functions
    self.sampler_table.itemChanged.connect(self.sampler_table_changed)
    self.sampler_table.horizontalHeader().sectionClicked.connect(self.sampler_table_header_clicked)

    #Setting the left part of the SAMPLER table (edge number, name, time)
    self.sampler_table.setItem(0, 0, QTableWidgetItem("0"))
    self.sampler_table.setItem(0, 1, QTableWidgetItem(self.experiment.sequence[0].name))
    self.sampler_table.setItem(0, 2, QTableWidgetItem(str(self.experiment.sequence[0].value)))
    delegate = ReadOnlyDelegate(self)
    for _ in range(3):
        exec("self.sampler_table.setItemDelegateForColumn(%d,delegate)" %_)

    
    #BUTTONS AT THE BOTTOM
    #button to stop continuous run
    self.stop_continuous_run_button_sampler = QPushButton(self.sampler_tab_widget)
    self.stop_continuous_run_button_sampler.setFont(QFont('Arial', 14))
    self.stop_continuous_run_button_sampler.setGeometry(10, 1060, 200, 30)
    self.stop_continuous_run_button_sampler.setText("Stop continuous run")
    self.stop_continuous_run_button_sampler.clicked.connect(self.stop_continuous_run_button_clicked)
    self.stop_continuous_run_button_sampler.setToolTip("Stop continuous run button stops whatever experiment was running before. It generates the init_hardware.py according to the latest default edge values and sets the hardware to that state. Again, it does not only stop continuous run, it stops any experiment and can be used to interrupt whatever was running.")
   
    #button to start continuous run
    self.continuous_run_button_sampler = QPushButton(self.sampler_tab_widget)
    self.continuous_run_button_sampler.setFont(QFont('Arial', 14))
    self.continuous_run_button_sampler.setGeometry(220, 1060, 200, 30)
    self.continuous_run_button_sampler.setText("Continuous run")
    self.continuous_run_button_sampler.clicked.connect(self.continuous_run_button_clicked)
    self.continuous_run_button_sampler.setToolTip("Continuous run button generates the experimental sequence description according to the current state of the Quatnrol as a run_experiment.py file and then runs that experimental sequence indefinitely.")
    
 
    #run experiment
    self.run_experiment_button_sampler = QPushButton(self.sampler_tab_widget)
    self.run_experiment_button_sampler.setFont(QFont('Arial', 14))
    self.run_experiment_button_sampler.setGeometry(430, 1060, 200, 30)
    self.run_experiment_button_sampler.setText("Run experiment")
    self.run_experiment_button_sampler.clicked.connect(self.run_experiment_button_clicked) 
    self.run_experiment_button_sampler.setToolTip("Run experiment button generates the experimental sequence description accodring to the current state of the Quantrol as a run_experiment.py file and then runs that experimental sequence once.")
    
    #go to edge
    self.go_to_edge_button_sampler = QPushButton(self.sampler_tab_widget)
    self.go_to_edge_button_sampler.setFont(QFont('Arial', 14))
    self.go_to_edge_button_sampler.setGeometry(640, 1060, 200, 30)
    self.go_to_edge_button_sampler.setText("Go to Edge")
    self.go_to_edge_button_sampler.clicked.connect(self.go_to_edge_button_clicked)
    self.go_to_edge_button_sampler.setToolTip("Go to Edge button is used to set the state of the hardware to a specific state at a particular edge. The user first needs to choose the edge to go by right clicking the sequence table on the left")


def mirny_tab_build(self):
    self.mirny_tab_num_cols = 6*config.mirny_channels_number + 3
    #MIRNY TABLE WIDGET
    self.mirny_tab_widget = QWidget()
    #MIRNY LABLE
    mirny_lable = QLabel(self.mirny_tab_widget)
    mirny_lable.setText("Mirny channels")
    mirny_lable.setFont(QFont('Arial', 14))
    mirny_lable.setGeometry(85, 0, 400, 30)
    self.sequence_num_rows = len(self.experiment.sequence)
    
    #MIRNY TAB LAYOUT
    self.mirny_table = QTableWidget(self.mirny_tab_widget)
    self.mirny_table.setGeometry(QRect(10, 30, 1905, 1020))
    self.mirny_table.setColumnCount(self.mirny_tab_num_cols)
    self.mirny_table.horizontalHeader().setMinimumHeight(50)
    self.mirny_table.verticalHeader().setVisible(False)
    self.mirny_table.horizontalHeader().setVisible(False)
    self.mirny_table.setRowCount(3) # 5 is an arbitrary number we just need to have rows in order to span them
    self.mirny_table.horizontalHeader().setMinimumSectionSize(0)
    self.mirny_table.setFont(QFont('Arial', 12))
    self.mirny_table.setFrameStyle(QFrame.NoFrame)
    #SHAPING THE FIRST 3 COLUMNS 
    self.mirny_table.setColumnWidth(0,50)
    self.mirny_table.setColumnWidth(1,180)
    self.mirny_table.setColumnWidth(2,100)
    self.mirny_table.setColumnWidth(3,5)

    delegate = ReadOnlyDelegate(self)
    #SHAPING THE TABLE
    for i in range(config.mirny_channels_number):
        self.mirny_table.setSpan(0,4 + 6*i, 1, 5) # stretching the title of the channel
        self.mirny_table.setColumnWidth(3 + 6*i, 5) # making separation line thin
        self.mirny_table.setColumnWidth(8 + 6*i, 45) # making state column smaller
        self.mirny_table.setItemDelegateForColumn(3 + 6*i,delegate) #making separation line uneditable
    
    #making first three columns verticaly wider to fit with header 
    for i in range(3):
        self.mirny_table.setSpan(0, i, 2, 1)
        self.mirny_table.setItemDelegateForColumn(i,delegate)
    #Filling the default values of MIRNY table
    for index, channel in enumerate(self.experiment.sequence[0].mirny):
        #plus 4 is because first 4 columns are used by number, name, time and separator(dark grey line)
        col = 4 + index * 6  
        for setting in range(5):
            exec("self.mirny_table.setItem(2, col + setting, QTableWidgetItem(str(channel.%s.expression)))" %self.setting_dict[setting])
            exec("self.mirny_table.item(2, col + setting).setToolTip(str(channel.%s.value))" %self.setting_dict[setting])
            if channel.state.value == 1:
                self.mirny_table.item(2, col + setting).setBackground(self.green)
            else:  
                self.mirny_table.item(2, col + setting).setBackground(self.red)


    self.mirny_table.itemChanged.connect(self.mirny_table_changed)

    #Dummy table that will display edge number, name and time and will be fixed (LEFT SIDE OF THE TABLE)
    self.mirny_dummy = QTableWidget(self.mirny_tab_widget)
    self.mirny_dummy.setGeometry(QRect(10,30,335,1003))
    self.mirny_dummy.setColumnCount(4)
    self.mirny_dummy.setRowCount(3)
    self.mirny_dummy.horizontalHeader().setMinimumHeight(50)
    self.mirny_dummy.verticalHeader().setVisible(False)
    self.mirny_dummy.horizontalHeader().setVisible(False)
    self.mirny_dummy.horizontalHeader().setMinimumSectionSize(0)
    self.mirny_dummy.horizontalHeader().setFont(QFont('Arial', 12))
    self.mirny_dummy.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.mirny_dummy.setFont(QFont('Arial', 12))
    self.mirny_dummy.setColumnWidth(0,50)
    self.mirny_dummy.setColumnWidth(1,180)
    self.mirny_dummy.setColumnWidth(2,100)
    self.mirny_dummy.setColumnWidth(3,5)
    self.mirny_dummy.setFrameStyle(QFrame.NoFrame)

    #making first three columns vertically wider to fit with header 
    for i in range(3):
        self.mirny_dummy.setSpan(0, i, 2, 1)
        self.mirny_dummy.setItemDelegateForColumn(i,delegate)
    #Filling the left part of the MIRNY table
    self.mirny_dummy.setItem(2, 0, QTableWidgetItem("0"))
    self.mirny_dummy.setItem(2, 1, QTableWidgetItem(self.experiment.sequence[0].name))
    self.mirny_dummy.setItem(2, 2, QTableWidgetItem(str(self.experiment.sequence[0].value)))


    #Dummy horizontal header (TOP SIDE OF THE TABLE)
    self.mirny_dummy_header = QTableWidget(self.mirny_tab_widget)
    self.mirny_dummy_header.setGeometry(QRect(10,30,1905,60))
    self.mirny_dummy_header.setColumnCount(self.mirny_tab_num_cols)
    self.mirny_dummy_header.horizontalHeader().setMinimumHeight(50)
    self.mirny_dummy_header.verticalHeader().setVisible(False)
    self.mirny_dummy_header.horizontalHeader().setVisible(False)
    self.mirny_dummy_header.setRowCount(2) 
    self.mirny_dummy_header.horizontalHeader().setMinimumSectionSize(0)
    self.mirny_dummy_header.horizontalHeader().setFont(QFont('Arial', 12))
    self.mirny_dummy_header.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.mirny_dummy_header.setFont(QFont('Arial', 12))
    self.mirny_dummy_header.setFrameStyle(QFrame.NoFrame)
    #SHAPING THE FIRST 3 COLUMNS 
    self.mirny_dummy_header.setColumnWidth(0,50) 
    self.mirny_dummy_header.setColumnWidth(1,180)
    self.mirny_dummy_header.setColumnWidth(2,100)

    #SHAPING THE TABLE
    for i in range(config.mirny_channels_number):
        self.mirny_dummy_header.setSpan(0,4 + 6*i, 1, 5) # stretching the title of the channel
        self.mirny_dummy_header.setColumnWidth(3 + 6*i, 5) # making separation line thin
        self.mirny_dummy_header.setColumnWidth(8 + 6*i, 45) # making state column smaller
        self.mirny_dummy_header.setItemDelegateForColumn(3 + 6*i,delegate) #making separation line uneditable

    self.mirny_dummy_header.setItemDelegateForRow(1, delegate) #making row number 2 uneditable

    #populating headers and separators
    for i in range(config.mirny_channels_number):
        #separator
        self.mirny_dummy_header.setSpan(0, 6*i + 3, self.sequence_num_rows+2, 1)
        self.mirny_dummy_header.setItem(0,6*i + 3, QTableWidgetItem())
        self.mirny_dummy_header.item(0, 6*i + 3).setBackground(self.grey)
        #headers Channel
        self.mirny_dummy_header.setItem(0,6*i+4, QTableWidgetItem(str(self.experiment.title_mirny_tab[i+4])))
        self.mirny_dummy_header.item(0,6*i+4).setTextAlignment(Qt.AlignCenter)
        #headers Channel attributes (f, Amp, att, phase, state)
        self.mirny_dummy_header.setItem(1,6*i+4, QTableWidgetItem('f (MHz)'))
        # self.mirny_dummy_header.setItem(1,6*i+5, QTableWidgetItem('Amp (dBm)'))
        self.mirny_dummy_header.setItem(1,6*i+6, QTableWidgetItem('Att (dBm)'))
        # self.mirny_dummy_header.setItem(1,6*i+7, QTableWidgetItem('phase (deg)'))
        self.mirny_dummy_header.setItem(1,6*i+8, QTableWidgetItem('state'))

    self.mirny_dummy_header.itemChanged.connect(self.mirny_dummy_header_changed)

    #Making fixed corner (TOP LEFT SIDE OF THE TABLE)
    self.mirny_fixed = QTableWidget(self.mirny_tab_widget)
    self.mirny_fixed.setGeometry(QRect(10,30, 335,60))
    self.mirny_fixed.setColumnCount(4)
    self.mirny_fixed.horizontalHeader().setMinimumHeight(50)
    self.mirny_fixed.verticalHeader().setVisible(False)
    self.mirny_fixed.horizontalHeader().setVisible(False)
    self.mirny_fixed.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.mirny_fixed.horizontalHeader().setMinimumSectionSize(0)
    self.mirny_fixed.setRowCount(2) 
    self.mirny_fixed.setFont(QFont('Arial', 12))
    self.mirny_fixed.setFrameStyle(QFrame.NoFrame)
    #SHAPING THE FIRST 3 COLUMNS
    self.mirny_fixed.setColumnWidth(0,50)
    self.mirny_fixed.setColumnWidth(1,180)
    self.mirny_fixed.setColumnWidth(2,100)
    self.mirny_fixed.setColumnWidth(3,5)
    #making first three columns vertically wider to fit with header 
    for i in range(4):
        self.mirny_fixed.setSpan(0, i, 2, 1)
        self.mirny_fixed.setItemDelegateForColumn(i,delegate)
    #Separator
    self.mirny_fixed.setItem(0,3, QTableWidgetItem())
    self.mirny_fixed.item(0,3).setBackground(self.grey)
    #populating edge number, name and time
    for i in range(3):
        self.mirny_fixed.setItem(0,i, QTableWidgetItem(str(self.experiment.title_mirny_tab[i])))
        self.mirny_fixed.item(0,i).setTextAlignment(Qt.AlignCenter)

    #MAKING VERTICAL SCROLL BARS COMMON FOR MIRNY TABLE
    self.mirny_tables = [self.mirny_table,self.mirny_dummy, self.analog_table,self.analog_dummy, self.digital_table, self.digital_dummy, self.sequence_table]

    def move_other_scrollbars_vertical(idx,bar):
        scrollbars = {tbl.verticalScrollBar() for tbl in self.mirny_tables}
        scrollbars.remove(bar)
        for bar in scrollbars:
            bar.setValue(idx)
        
    self.mirny_dummy.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.mirny_dummy.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    for tbl in self.mirny_tables:
        scrollbar = tbl.verticalScrollBar()
        scrollbar.valueChanged.connect(lambda idx,bar=scrollbar: move_other_scrollbars_vertical(idx, bar))

    #MAKING HORIZONTAL SCROLL BARS COMMON FOR MIRNY TABLE
    self.mirny_dummy_tables = [self.mirny_table,self.mirny_dummy_header]

    def move_other_scrollbars_horizontal(idx,bar):
        scrollbars = {tbl.horizontalScrollBar() for tbl in self.mirny_dummy_tables}
        scrollbars.remove(bar)
        for bar in scrollbars:
            bar.setValue(idx)
        
    self.mirny_dummy_header.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.mirny_dummy_header.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    for tbl in self.mirny_dummy_tables:
        scrollbar = tbl.horizontalScrollBar()
        scrollbar.valueChanged.connect(lambda idx,bar=scrollbar: move_other_scrollbars_horizontal(idx, bar))

    
    #BUTTONS AT THE BOTTOM
    #button to stop continuous run
    self.stop_continuous_run_button_mirny = QPushButton(self.mirny_tab_widget)
    self.stop_continuous_run_button_mirny.setFont(QFont('Arial', 14))
    self.stop_continuous_run_button_mirny.setGeometry(10, 1060, 200, 30)
    self.stop_continuous_run_button_mirny.setText("Stop continuous run")
    self.stop_continuous_run_button_mirny.clicked.connect(self.stop_continuous_run_button_clicked)
    self.stop_continuous_run_button_mirny.setToolTip("Stop continuous run button stops whatever experiment was running before. It generates the init_hardware.py according to the latest default edge values and sets the hardware to that state. Again, it does not only stop continuous run, it stops any experiment and can be used to interrupt whatever was running.")
   
    #button to start continuous run
    self.continuous_run_button_mirny = QPushButton(self.mirny_tab_widget)
    self.continuous_run_button_mirny.setFont(QFont('Arial', 14))
    self.continuous_run_button_mirny.setGeometry(220, 1060, 200, 30)
    self.continuous_run_button_mirny.setText("Continuous run")
    self.continuous_run_button_mirny.clicked.connect(self.continuous_run_button_clicked)
    self.continuous_run_button_mirny.setToolTip("Continuous run button generates the experimental sequence description according to the current state of the Quatnrol as a run_experiment.py file and then runs that experimental sequence indefinitely.")
 
    #run experiment
    self.run_experiment_button_mirny = QPushButton(self.mirny_tab_widget)
    self.run_experiment_button_mirny.setFont(QFont('Arial', 14))
    self.run_experiment_button_mirny.setGeometry(430, 1060, 200, 30)
    self.run_experiment_button_mirny.setText("Run experiment")
    self.run_experiment_button_mirny.clicked.connect(self.run_experiment_button_clicked) 
    self.run_experiment_button_mirny.setToolTip("Run experiment button generates the experimental sequence description accodring to the current state of the Quantrol as a run_experiment.py file and then runs that experimental sequence once.")
    
    #go to edge
    self.go_to_edge_button_mirny = QPushButton(self.mirny_tab_widget)
    self.go_to_edge_button_mirny.setFont(QFont('Arial', 14))
    self.go_to_edge_button_mirny.setGeometry(640, 1060, 200, 30)
    self.go_to_edge_button_mirny.setText("Go to Edge")
    self.go_to_edge_button_mirny.clicked.connect(self.go_to_edge_button_clicked)
    self.go_to_edge_button_mirny.setToolTip("Go to Edge button is used to set the state of the hardware to a specific state at a particular edge. The user first needs to choose the edge to go by right clicking the sequence table on the left")


def slow_dds_tab_build(self):
    self.slow_dds_tab_num_cols = 6*config.slow_dds_channels_number
    #SLOW_DDS TABLE WIDGET
    self.slow_dds_tab_widget = QWidget()
    #SLOW_DDS LABLE
    slow_dds_lable = QLabel(self.slow_dds_tab_widget)
    slow_dds_lable.setText("Slow_dds channels")
    slow_dds_lable.setFont(QFont('Arial', 14))
    slow_dds_lable.setGeometry(85, 0, 400, 30)
    self.sequence_num_rows = len(self.experiment.sequence)
    
    #SLOW_DDS TAB LAYOUT
    self.slow_dds_table = QTableWidget(self.slow_dds_tab_widget)
    self.slow_dds_table.setGeometry(QRect(10, 30, 1905, 1020))
    self.slow_dds_table.setColumnCount(self.slow_dds_tab_num_cols)
    self.slow_dds_table.horizontalHeader().setMinimumHeight(50)
    self.slow_dds_table.verticalHeader().setVisible(False)
    self.slow_dds_table.horizontalHeader().setVisible(False)
    self.slow_dds_table.setRowCount(3) 
    self.slow_dds_table.horizontalHeader().setMinimumSectionSize(0)
    self.slow_dds_table.setFont(QFont('Arial', 12))
    self.slow_dds_table.setFrameStyle(QFrame.NoFrame)

    delegate = ReadOnlyDelegate(self)
    #SHAPING THE TABLE
    for i in range(config.slow_dds_channels_number):
        self.slow_dds_table.setSpan(0,1 + 6*i, 1, 5) # stretching the title of the channel
        self.slow_dds_table.setColumnWidth(6*i, 5) # making separation line thin
        self.slow_dds_table.setColumnWidth(5 + 6*i, 45) # making state column smaller
        self.slow_dds_table.setItemDelegateForColumn(6*i,delegate) #making separation line uneditable
    
    for index, channel in enumerate(self.experiment.slow_dds):
        col = index * 6 + 1 # there is a separator in the very beginning
        for setting in range(5):
            exec("self.slow_dds_table.setItem(2, col + setting, QTableWidgetItem(str(channel.%s)))" %self.setting_dict[setting])
            exec("self.slow_dds_table.item(2, col + setting).setToolTip(str(channel.%s))" %self.setting_dict[setting])
            if channel.state == 1:
                self.slow_dds_table.item(2, col + setting).setBackground(self.green)
            else:  
                self.slow_dds_table.item(2, col + setting).setBackground(self.red)
                
    self.slow_dds_table.setItemDelegateForRow(1, delegate) #making row number 2 uneditable
    self.slow_dds_table.itemChanged.connect(self.slow_dds_table_changed)

    #populating headers and separators
    for i in range(config.slow_dds_channels_number):
        #separator
        self.slow_dds_table.setSpan(0, 6*i, self.sequence_num_rows+2, 1)
        self.slow_dds_table.setItem(0, 6*i, QTableWidgetItem())
        self.slow_dds_table.item(0, 6*i).setBackground(self.grey)
        #headers Channel
        self.slow_dds_table.setItem(0,6*i + 1, QTableWidgetItem(str(self.experiment.title_slow_dds_tab[i+4])))
        self.slow_dds_table.item(0,6*i + 1).setTextAlignment(Qt.AlignCenter)
        #headers Channel attributes (f, Amp, att, phase, state)
        self.slow_dds_table.setItem(1,6*i + 1, QTableWidgetItem('f (MHz)'))
        self.slow_dds_table.setItem(1,6*i + 2, QTableWidgetItem('Amp (dBm)'))
        self.slow_dds_table.setItem(1,6*i + 3, QTableWidgetItem('Att (dBm)'))
        self.slow_dds_table.setItem(1,6*i + 4, QTableWidgetItem('phase (deg)'))
        self.slow_dds_table.setItem(1,6*i + 5, QTableWidgetItem('state'))

    #button to set slow dds states
    self.set_slow_dds_states = QPushButton(self.slow_dds_tab_widget)
    self.set_slow_dds_states.setFont(QFont('Arial', 14))
    self.set_slow_dds_states.setGeometry(10, 150, 200, 30)
    self.set_slow_dds_states.setText("Set slow DDS states")
    self.set_slow_dds_states.clicked.connect(self.set_slow_dds_states_button_clicked)
    self.set_slow_dds_states.setToolTip("Set slow dds states button is used to prepare the experimental description and run it to set the states of only the slow dds channels. Any experiment that has been running at the time of pressing this button will be interrupted and might leave the experiment in a random state that might be not safe. It is a user responsibility to make sure that this button is clicked only when there is no experiment running. This should be fine since this DDSs should be used permanently and only changed quite rarely.")
