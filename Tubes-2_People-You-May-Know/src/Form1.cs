using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

// Tugas besar 2: Pengaplikasian Algoritma BFS dan DFS pada fitur People You May Know jejaring sosial Facebook
// Kelompok Social Distancing v2 IF2211 Strategi Algoritma 2021
// Prana Gusriana (13519195)
// Nabil Nabighah (13519168)
// Rais Vaza Man Tazakka (13519060)

namespace TubesStima2
{
    public partial class Form1 : Form
    {
        //atribut Form1
        OpenFileDialog ofd = new OpenFileDialog();
        //create a form 
        System.Windows.Forms.Form form = new System.Windows.Forms.Form();
        //create a viewer object 
        Microsoft.Msagl.GraphViewerGdi.GViewer viewer = new Microsoft.Msagl.GraphViewerGdi.GViewer();
        //create a graph object 
        Microsoft.Msagl.Drawing.Graph graph = new Microsoft.Msagl.Drawing.Graph("graph");
        Graph gr = new Graph();
        public Form1()
        {
            InitializeComponent();
            this.BackgroundImage = Properties.Resources.bg;
        }

        // readfile from path
        void readFile()
        {
            gr.clearAll();
            graph = new Microsoft.Msagl.Drawing.Graph("graph");
            //save path file from browse to path
            string path = this.ofd.FileName;
            //read file per line, setiap line baru index array baru
            string[] array = System.IO.File.ReadAllLines(path);
            //List<char> arrayfix = new List<char>();
            int indexmax = int.Parse(array[0]);
            for (int i = 1; i <= indexmax; i++) 
            {
                string vS = "";
                string vD = "";
                int j = 0;
                
                while (array[i][j] != ' ' && j < array[i].Length)
                {
                    vS += array[i][j];   
                    j++; 
                }

                j++;
                while (j < array[i].Length){
                    vD += array[i][j];
                    j++;
                }
                gr.addEdge(vS, vD);
                graph.AddEdge(vS, vD).Attr.ArrowheadAtTarget = Microsoft.Msagl.Drawing.ArrowStyle.None;
                Microsoft.Msagl.Drawing.Node a = graph.FindNode(vS);
                Microsoft.Msagl.Drawing.Node b = graph.FindNode(vD);
                a.Attr.Shape = Microsoft.Msagl.Drawing.Shape.Circle;
                b.Attr.Shape = Microsoft.Msagl.Drawing.Shape.Circle;
            }
            //create the graph content 
            Microsoft.Msagl.Drawing.Node c = graph.FindNode("A");
            //bind the graph to the viewer 
            graph.Directed = false;
            viewer.Graph = graph;
            //associate the viewer with the form 
            panel1.SuspendLayout();
            viewer.Dock = System.Windows.Forms.DockStyle.Fill;
            viewer.CalculateLayout(graph);
            viewer.SaveButtonVisible = false;
            viewer.SaveGraphButtonVisible = false;
            viewer.UndoRedoButtonsVisible = false;
            viewer.LayoutAlgorithmSettingsButtonVisible = false;
            viewer.AutoSize = true;
            viewer.AutoScroll = true;
            panel1.Controls.Add(viewer);
            panel1.ResumeLayout();
        }

        //add Node to Choose Account list
        void addNodeAccount()
        {
            List<string> listNode = new List<string>();
            listNode = gr.getGraph();
            foreach (string node in listNode)
            {
                cmbAccount.Items.Add(node);
            }
        }

        // Menambahkan nama akun yang belum berteman dengan akun yang dipilih untuk dapat di explore
        void addNodeExplore() 
        {
            List<string> listNode = new List<string>();
            listNode = gr.getGraph();
            string getaccount = cmbAccount.SelectedItem.ToString();
            List<string> listAdjacent = gr.getAdjacent(getaccount);
            foreach (string node in listNode)
            {
                if (node != getaccount && !(listAdjacent.Contains(node)))
                {
                    cmbExplore.Items.Add(node);
                }
            }
        }
       
        
        // Browse File button
        private void button1_Click(object sender, EventArgs e)
        {
            textBox1.Text = "";
            textBox2.Text = "";
            textBox3.Text = "";
            gr.clearAll();
            cmbExplore.Items.Clear();
            cmbAccount.Items.Clear();
            // filter to only open file that we want (.txt)
            ofd.Filter = "TXT File|*.txt";
            // ofd.ShowDialog(); = open File Browse
            if (ofd.ShowDialog() == DialogResult.OK) // continue with the code if user select file
            {
                // show save file name to textBox1
                textBox1.Text = ofd.SafeFileName;
                // put file path to 
                readFile();
                addNodeAccount();
            }
            
        }
        
        
        // Submit Button
        private void button2_Click(object sender, EventArgs e)
        {
            // CHOOSE ALGORITHM
            string getMethod = cmbAlgorithm.SelectedItem.ToString();
            // CHOOSE ACCOUNT
            string getAccount = cmbAccount.SelectedItem.ToString();
            // EXPLORE FRIEND WITH
            string getExplore = cmbExplore.SelectedItem.ToString();

            textBox2.Text = "\r\n" + gr.friendRecommendation(getAccount, getMethod); // Show friend recommendation
            textBox3.Text = "\r\n" + gr.exploreFriendship(getAccount, getExplore, getMethod); // Show explore friend

            // Visualisasi explore friend, bikin graf baru
            List<List<string>> ls = gr.getSolutionPath();
            List<string> dg = gr.getGraph();
            Microsoft.Msagl.Drawing.Graph graphTemp = new Microsoft.Msagl.Drawing.Graph("graphTemp");
            string path = this.ofd.FileName;
            string[] array = System.IO.File.ReadAllLines(path);
            int indexmax = int.Parse(array[0]);
            for (int i = 1; i <= indexmax; i++)
            {
                string vS = "";
                string vD = "";
                int j = 0;

                while (array[i][j] != ' ' && j < array[i].Length)
                {
                    vS += array[i][j];
                    j++;
                }

                j++;
                while (j < array[i].Length)
                {
                    vD += array[i][j];
                    j++;
                }
                bool exist = false;
                int p = 0;
                if (ls.Count > 0)
                {
                    while (p < (ls[0].Count - 1) && !exist)
                    {
                        if ((vS == ls[0][p] && vD == ls[0][p + 1]) || (vD == ls[0][p] && vS == ls[0][p + 1]))
                        {
                            exist = true;
                        }
                        else
                        {
                            p++;
                        }
                    }
                }
                if (!exist) // Jika Edge yang ditambahkan bukan merupakan jalur explore friend, tidak akan diberi warna
                {
                    graphTemp.AddEdge(vS, vD).Attr.ArrowheadAtTarget = Microsoft.Msagl.Drawing.ArrowStyle.None;
                    Microsoft.Msagl.Drawing.Node a = graphTemp.FindNode(vS);
                    Microsoft.Msagl.Drawing.Node b = graphTemp.FindNode(vD);
                    a.Attr.Shape = Microsoft.Msagl.Drawing.Shape.Circle;
                    b.Attr.Shape = Microsoft.Msagl.Drawing.Shape.Circle;
                }
                else
                {
                    var gt = graphTemp.AddEdge(vS, vD);
                    gt.Attr.ArrowheadAtTarget = Microsoft.Msagl.Drawing.ArrowStyle.None;
                    if (vS == ls[0][p] && vD == ls[0][p + 1])
                    {
                        gt.Attr.ArrowheadAtTarget = Microsoft.Msagl.Drawing.ArrowStyle.Normal;
                    }
                    else
                    {
                        gt.Attr.ArrowheadAtSource = Microsoft.Msagl.Drawing.ArrowStyle.Normal;
                    }
                    gt.Attr.Color = Microsoft.Msagl.Drawing.Color.Red;
                    Microsoft.Msagl.Drawing.Node a = graphTemp.FindNode(vS);
                    Microsoft.Msagl.Drawing.Node b = graphTemp.FindNode(vD);
                    a.Attr.Shape = Microsoft.Msagl.Drawing.Shape.Circle;
                    b.Attr.Shape = Microsoft.Msagl.Drawing.Shape.Circle;
                    a.Attr.FillColor = Microsoft.Msagl.Drawing.Color.DeepSkyBlue;
                    b.Attr.FillColor = Microsoft.Msagl.Drawing.Color.DeepSkyBlue;
                }
            }
            // Tampilkan visualisasi pada panel
            viewer.Graph = graphTemp;
            panel1.Controls.Clear();
            panel1.SuspendLayout();
            viewer.Dock = System.Windows.Forms.DockStyle.Fill;
            viewer.AutoSize = true;
            viewer.AutoScroll = true;
            panel1.Controls.Add(viewer);
            panel1.ResumeLayout();
        }

        //ADD NODE EXPLORE TO COMBOBOX
        private void cmbAccount_SelectedIndexChanged(object sender, EventArgs e)
        {
            cmbExplore.Items.Clear();
            addNodeExplore();
        }

        private void button3_Click(object sender, EventArgs e)
        {
            cmbExplore.Items.Clear();
            cmbAccount.Items.Clear();
            panel1.Controls.Clear();
            textBox1.Text = "";
            textBox2.Text = "";
            textBox3.Text = "";
            cmbAlgorithm.SelectedIndex = -1;
            cmbExplore.SelectedIndex = -1;
            cmbAccount.SelectedIndex = -1;
        }

        private void textBox3_TextChanged(object sender, EventArgs e)
        {

        }
    }
}
