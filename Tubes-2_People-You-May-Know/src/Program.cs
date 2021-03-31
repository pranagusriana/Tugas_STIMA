using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;

// Tugas besar 2: Pengaplikasian Algoritma BFS dan DFS pada fitur People You May Know jejaring sosial Facebook
// Kelompok Social Distancing v2 IF2211 Strategi Algoritma 2021
// Prana Gusriana (13519195)
// Nabil Nabighah (13519168)
// Rais Vaza Man Tazakka (13519060)

namespace TubesStima2
{
    public class Graph
    {
        private Dictionary<string, List<string>> graph;
        private Dictionary<string, bool> visited;
        private Queue<List<string>> queue;
        private List<List<string>> solutionPath;

        //ctor class graph
        public Graph()
        {
            this.graph = new Dictionary<string, List<string>>();
            this.visited = new Dictionary<string, bool>();
            this.queue = new Queue<List<string>>();
            this.solutionPath = new List<List<string>>();
        }

        // Method untuk menambah sisi dari Vs (Vertex source) ke Vd (Vertex destination), reperesentasi adjacency list
        public void addEdge(string Vs, string Vd)
        {
            if (!this.graph.ContainsKey(Vs))
            {
                this.graph[Vs] = new List<string>();
            }
            this.graph[Vs].Add(Vd);
            if (!this.graph.ContainsKey(Vd))
            {
                this.graph[Vd] = new List<string>();
            }
            this.graph[Vd].Add(Vs);

        }

        // Mengurutkan prioritas adjacent yang dimiliki suatu simpul berdasarkan abjad
        public void sortPriority()
        {
            foreach (string key in this.graph.Keys)
            {
                this.graph[key].Sort();
            }
        }

        // Method algoritma BFS, hasilnya atribut solutionPath terisi
        public void BFS(string Vfirst, string Vgoal)
        {
            this.queue.Clear();
            this.visited.Clear();
            this.solutionPath.Clear();
            this.queue.Enqueue(new List<string>() { Vfirst });
            this.sortPriority();
            foreach (string key in this.graph.Keys)
            {
                this.visited[key] = false;
            }
            while (this.queue.Count() > 0)
            {
                List<string> path = this.queue.Dequeue();
                string Vcurr = path[path.Count - 1];
                this.visited[Vcurr] = true;
                if (Vcurr == Vgoal)
                {
                    this.solutionPath.Add(path);
                }
                foreach (string adjacent in this.graph[Vcurr])
                {
                    if (this.visited[adjacent] == false)
                    {
                        List<string> newPath = path.ToList();
                        newPath.Add(adjacent);
                        this.queue.Enqueue(newPath);
                    }
                }
            }
        }

        public void DFShelper(string Vcurr, string Vgoal, List<string> currPath)
        {
            this.visited[Vcurr] = true;
            currPath.Add(Vcurr);
            if (Vcurr == Vgoal)
            {
                this.solutionPath.Add(currPath.ToList());
            }
            else
            {
                foreach (string adjacent in this.graph[Vcurr])
                {
                    if (this.visited[adjacent] == false)
                    {
                        this.DFShelper(adjacent, Vgoal, currPath);
                    }
                }
            }
            currPath.RemoveAt(currPath.Count - 1);
            this.visited[Vcurr] = false;
        }

        // Algoritma DFS, hasilnya atribut solutionPath terisi
        public void DFS(string Vcurr, string Vgoal)
        {
            this.visited.Clear();
            this.solutionPath.Clear();
            foreach (string key in this.graph.Keys)
            {
                this.visited[key] = false;
            }
            this.sortPriority();
            List<string> currPath = new List<string>();
            this.DFShelper(Vcurr, Vgoal, currPath);
        }

        // Method untuk menampilkan friend recommendation untuk akun inputVal, dan menghasilkan output berupa string
        public string friendRecommendation(string inputVal, string typeAlgorithm)
        {
            string ret = "";
            Dictionary<string, List<List<string>>> fr = new Dictionary<string, List<List<string>>>();
            foreach (string key in this.graph.Keys)
            {
                if (key != inputVal && !(this.graph[inputVal].Contains(key)))
                {
                    if (typeAlgorithm == "BFS")
                    {
                        this.BFS(inputVal, key);
                    }
                    else
                    {
                        this.DFS(inputVal, key);
                    }
                    List<List<string>> temp = new List<List<string>>();
                    foreach (List<string> listSol in this.solutionPath)
                    {
                        if (listSol.Count == 3)
                        {
                            temp.Add(listSol);
                        }
                    }
                    if (temp.Count != 0)
                    {
                        fr[key] = temp;
                    }
                }
            }
            Dictionary<string, int> frsort = new Dictionary<string, int>();
            foreach (string keyS in fr.Keys)
            {
                frsort[keyS] = fr[keyS].Count;
            }
            frsort = frsort.OrderByDescending(key => key.Value).ToDictionary(x => x.Key, x => x.Value);
            if (fr.Count() == 0)
            {
                ret += "Tidak terdapat rekomendasi teman untuk akun " + inputVal;
            }
            else
            {
                ret += "Daftar rekomendasi teman untuk akun " + inputVal + ": \r\n";
            }
            foreach (string keyS2 in frsort.Keys)
            {
                ret += "Nama akun: " + keyS2 + "\r\n";
                ret += frsort[keyS2] + " mutual friends \r\n";
                foreach (List<string> lval in fr[keyS2])
                {
                    ret += lval[1] + "\r\n";
                }
                ret += "\r\n";
            }
            return ret;
        }

        // Method untuk mendapatkan solusi
        public List<List<string>> getSolutionPath()
        {
            return this.solutionPath;
        }

        // Method untuk menampilkan semua simpul yang dimiliki suatu graf
        public void printInfo()
        {
            foreach (string line in this.graph.Keys)
            {
                System.Console.WriteLine(line);
            }
        }

        // Method untuk menampilkan explore friend, menghasilkan output string yang berisi konten yang akan ditampilkan pada explore friend
        public string exploreFriendship(string VA, string VB, string typeAlgorithm)
        {
            string ret = "";
            ret += "Nama akun: " + VA + " dan " + VB +  "\r\n";
            if (typeAlgorithm == "DFS")
            {
                this.DFS(VA, VB);
            }
            else
            {
                this.BFS(VA, VB);
            }

            if (this.solutionPath.Count() != 0)
            {
                ret += (this.solutionPath[0].Count() - 2);
                if ((this.solutionPath[0].Count() - 2) % 10 == 1)
                {
                    ret += "st";
                }
                else if ((this.solutionPath[0].Count() - 2) % 10 == 2)
                {
                    ret += "nd";
                }
                else if ((this.solutionPath[0].Count() - 2) % 10 == 3)
                {
                    ret += "rd";
                }
                else
                {
                    ret += "th";
                }
                ret += "-degree connection \r\n";
                foreach (string vertex in this.solutionPath[0])
                {
                    if (vertex == VB)
                    {
                        ret += vertex;
                    }
                    else
                    {
                        ret += vertex + " -> ";
                    }
                }
            }
            else
            {
                ret += "Tidak ada jalur koneksi yang tersedia \r\n Anda harus memulai koneksi baru itu sendiri";
            }
            return ret;
        }

        // return list of keys
        public List<string> getGraph()
        {
            List<string> arrayNode = new List<string>();
            foreach (string node in this.graph.Keys)
            {
                arrayNode.Add(node);
            }
            return arrayNode;
        }

        // Method untuk mendapatkan array adjacent dari suatu simpul, Asumsi input V selalu valid (ada di graph)
        public List<string> getAdjacent(string V)
        {
            List<string> arrayAdjacent = new List<string>();
            foreach(string adjacent in this.graph[V])
            {
                arrayAdjacent.Add(adjacent);
            }
            return arrayAdjacent;
        }

        // Method untuk mengosongkan semua attribute
        public void clearAll()
        {
            this.graph.Clear();
            this.visited.Clear();
            this.queue.Clear();
            this.solutionPath.Clear();
        }
    }

    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new Form1());
        }
    }    
}

