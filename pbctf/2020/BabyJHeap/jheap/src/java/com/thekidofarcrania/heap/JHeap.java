package com.thekidofarcrania.heap;

import java.io.*;
import java.util.*;
import java.util.function.*;

import static java.lang.System.*;

public class JHeap {
  private static String the_flag;

  public static class HeapAction {
    public Consumer<Integer> action;
    public String name;

    public HeapAction(Consumer<Integer> action, String name) {
      this.action = action;
      this.name = name;
    }

    public void printChoice(int num) {
      out.println(num + ". " + name);
    }
  }

  private static Scanner in = new Scanner(System.in);
  private static JHeap arr[] = new JHeap[0x30];
  private static ArrayList<Object> spray = new ArrayList<>();

  public static void edit(int ind) { arr[ind].editThis(0x1337); }
  public static void delete(int ind) { arr[ind] = null; }
  public static void view(int ind) { arr[ind].viewThis(); }
  public static void leak(int ind) { arr[ind].flag = the_flag; }

  // For debugging purposes :)
  private static native long addrOf(Object o);

  public static void subaction(int ind) {
    Runnable subactions[] = {
      new Runnable() {
        public void run() {
          System.exit(0);
        }
      }, 
      new Runnable() {
        public void run() {
          System.out.println("Version: JHeap v1.0");
        }
      }
    };

    subactions[ind].run();
  }

  static {
    System.load(System.getProperty("java.home") + "/lib/libheap.so");
    for (int i = 0; i < 100; i++)
      spray.add(new char[(int)(Math.random() * 1337)]);
    for (int i = 0; i < arr.length; i++)
      arr[i] = new JHeap(i);
//    for (int i = 0; i < arr.length; i++)
//      arr[i].dump();
    for (int i = 0; i < 100; i++)
      spray.add(new char[(int)(Math.random() * 1337)]);
  }

  private String flag;
  private char[] data;
  private int ind;

  private JHeap(int ind) {
    if (arr[ind] != null) 
      throw new IllegalArgumentException("Already taken!");

    arr[ind] = this;
    this.ind = ind;
    this.data = new char[(int)(Math.random() * 1337)];
  }

  private void dump() {
    out.printf("Heap[%02d] (0x%016x) = char[] @ 0x%016x\n", ind, 
        addrOf(this), addrOf(data));
  }
  
  private int utf8Length() {
    try { 
      return (new String(data)).getBytes("utf-8").length;
    } catch (UnsupportedEncodingException e) {
      return 0;
    }
  }

  private native void editThis(int x);

  private void viewThis() {
    out.println("*****************************");
    out.println("Heap[" + ind + "] = " + new String(data));
    out.println("*****************************");
  }

  public static void main(String[] args) throws Exception {
    HeapAction actions[] = {
      new HeapAction(JHeap::edit, "edit"),
      new HeapAction(JHeap::view, "view"),
      new HeapAction(JHeap::leak, "leak"),
      new HeapAction(JHeap::subaction, "subaction")
    };

    try {
      Scanner flag = new Scanner(new File("/flag"));
      the_flag = flag.next(); 
    } catch (IOException e) {
      System.out.println("Failed to load flag!");
      System.exit(1);
    }


    while (true) {
      int act, ind = 0;

      out.println(">>> JHeap <<<");
      for (int i = 0; i < actions.length; i++) {
        actions[i].printChoice(i);
      }

      out.print("> ");
      act = in.nextInt();
      if (act < 0 || act >= actions.length) {
        out.println("Invalid choice!");
        continue;
      }

      out.print("Index: ");
      ind = in.nextInt();

      in.nextLine();

      actions[act].action.accept(ind);
    }
  }
}
