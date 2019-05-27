using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;

namespace Snake
{
    class Colors
    {
        public static Brush SnakeColor { get; set; }
        public static Brush AppleColor { get; set; }

        public Colors()
        {
            SnakeColor = Brushes.Black;
            AppleColor = Brushes.Red;
        }
    }
}
