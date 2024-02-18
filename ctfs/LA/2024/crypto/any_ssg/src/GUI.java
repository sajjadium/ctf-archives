import javax.swing.JFrame;
import javax.swing.JButton;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.JLabel;
import javax.swing.JTextArea;
import java.awt.BorderLayout;
import java.awt.GridLayout;
import java.util.Hashtable;
import java.awt.Toolkit;
import java.awt.Dimension;
import java.awt.event.*;
import java.awt.Color;
import java.awt.Font;
import javax.swing.SwingConstants;

public class GUI implements KeyListener {

    private Game game;
    private Board board;
    private JFrame frame;

    public void run() {
        frame = new JFrame("My new game");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(800, 100);

        JPanel panel = new JPanel();
        JLabel label = new JLabel("Enter Seed");
        JTextField tf = new JTextField(19);
        JButton send = new JButton("Send");
        JButton reset = new JButton("Reset");
        panel.add(label);
        panel.add(tf);
        panel.add(send);
        panel.add(reset);

        frame.add(panel);
        frame.setVisible(true);
        frame.setFocusable(true);

        reset.addActionListener(e -> tf.setText(""));

        send.addActionListener(e -> {
            String seed = tf.getText();
            if (isNumeric(seed) || seed.equals("")) {
                if (seed.equals("")) {
                    setGame(new Game());
                }
                else {
                    setGame(new Game(Long.parseLong(seed)));
                }
                setBoard(game.getBoard());
                drawGame(board);
                frame.addKeyListener(this);
            }
            else {
                tf.setText("Error: invalid seed");
            }
        });

    }

    private void setGame(Game g) { 
        game = g;
    }

    private void setBoard(Board b) {
        board = b;
    }

    public boolean isNumeric(String str) {
        try {
            Long.parseLong(str);
            return true;
        } catch(NumberFormatException e){
            return false;
        }
    }

    private void drawGame(Board b) {
        Dimension size = Toolkit.getDefaultToolkit().getScreenSize();
        int h = (int)size.getHeight();
        int w = (int)size.getWidth();
        int s = 9*(Math.min(h, w))/10;
        frame.setSize(s,s);
        frame.getContentPane().removeAll();


        GridLayout blocks = new GridLayout(b.getSizeX(),b.getSizeY());
        frame.setLayout(blocks);

        update();


        frame.repaint();
        frame.setVisible(true);
    }

    private void update() {
        if (board.getPlayer().getCurrentTile().getName().equals("end_portal")) {
            win();
        }
        else if (board.getPlayer().getCurrentTile().getName().equals("lava")) {
            dead();
        }
        else {
            Hashtable<String, Color> colorTable = new Hashtable<>();
            colorTable.put("grass", new Color(74,126,43));
            colorTable.put("water", new Color(36,71,111));
            colorTable.put("stone", new Color(69,69,69));
            colorTable.put("lava", new Color(213,67,2));
            colorTable.put("end_portal_frame", new Color(53,92,82));
            colorTable.put("end_portal", new Color(4,14,28));


            for (int i = 0; i < board.getSizeX(); i++) {
                for (int j = 0; j < board.getSizeY(); j++) {
                    boolean playerHere = false;
                    String text = "";
                    Color foregroundColor = Color.BLACK;

                    if (board.getTile(i, j).getName().equals("end_portal_frame")) {
                        text = "●";
                        if (board.getTile(i,j).getFilled()) {
                            foregroundColor = new Color(129,184,114);
                        }
                    }
                    if (i == board.getPlayer().getX() && j == board.getPlayer().getY()) {
                        text = "+";
                        foregroundColor = Color.BLACK;
                        playerHere = true;
                    }
                    JLabel block = new JLabel(text);
                    block.setVerticalAlignment(SwingConstants.CENTER);
                    block.setHorizontalAlignment(SwingConstants.CENTER);
                    block.setFont(new Font("Arial", Font.BOLD, 10));
                    block.setForeground(foregroundColor);
                    block.setBackground(colorTable.get(board.getTile(i,j).getName()));
                    if (playerHere) {
                        block.setBackground(Color.RED);
                    }
                    block.setOpaque(true);
                    frame.add(block);
                }
            }
        }

    }

    private void dead() {
        frame.getContentPane().removeAll();
        frame.setLayout(new BorderLayout());
        JTextArea ta = new JTextArea("You died! :( \n\nTry again. Hopefully your next seed will be more lucky!");
        ta.setFont(new Font("Arial", Font.BOLD, 40));
        ta.setLineWrap(true);
        ta.setWrapStyleWord(true);
        frame.add(ta);
        frame.repaint();
        frame.setVisible(true);

    }

    private void win() {
        frame.getContentPane().removeAll();
        frame.setLayout(new BorderLayout());
        JTextArea ta = new JTextArea("Congrats on beating the game (for now)! We may or may not implement a dragon fight in the future... \n\nFor now, submit your seed to the netcat connection in the challenge to receive your flag!");
        ta.setFont(new Font("Arial", Font.BOLD, 40));
        ta.setLineWrap(true);
        ta.setWrapStyleWord(true);
        frame.add(ta);
        frame.repaint();
        frame.setVisible(true);

    }

    public void keyPressed (KeyEvent e) {
    }
    public void keyReleased (KeyEvent e) {
    }
    public void keyTyped (KeyEvent e) {
        switch (e.getKeyChar()) {
            case 'a' -> game.onA();
            case 's' -> game.onS();
            case 'w' -> game.onW();
            case 'd' -> game.onD();
        }
        drawGame(board);
    }


}
