package com.example.pokedex.ui.main;

import android.graphics.Color;

import java.util.HashMap;

public class Info {
    public static HashMap<String, Integer> nameToInt;
    public static HashMap<Integer, String> intToType1;
    public static HashMap<Integer, String> intToType2;
    public static HashMap<Integer, String > intToData;
    public static HashMap<String, String > typeColor;
    Info()
    {

        nameToInt = new HashMap<>();
        intToType1 = new HashMap<>();
        intToType2 = new HashMap<>();
        intToData = new HashMap<>();
        typeColor = new HashMap<>();
        String[] names = {"Blastoise","Blaziken","Charizard","Chesnaught","Delphox", "Greninja", "Pikachu", "Sceptile", "Swampert", "Venusaur"};
        String[] type1 = {"Water","Fire","Fire","Grass","Fire","Water","Electric","Grass","Water","Grass"};
        String[] type2 = {"Nan","Fighting","Flying","Fighting","Psychic","Dark","Nan","Nan","Ground","Poison"};
        String[] data = {"Blastoise has water spouts that protrude from its shell. The water spouts are very accurate. They can shoot bullets of water with enough accuracy to strike empty cans from a distance of over 160 feet. ",
        "In battle, Blaziken blows out intense flames from its wrists and attacks foes courageously. The stronger the foe, the more intensely this Pokémon's wrists burn. ",
        "Charizard flies around the sky in search of powerful opponents. It breathes fire of such great heat that it melts anything. However, it never turns its fiery breath on any opponent weaker than itself. ",
        "Its Tackle is forceful enough to flip a 50-ton tank. It shields its allies from danger with its own body. ",
        "It gazes into the flame at the tip of its branch to achieve a focused state, which allows it to see into the future. ",
        "It creates throwing stars out of compressed water. When it spins them and throws them at high speed, these stars can split metal in two. ",
        "Whenever Pikachu comes across something new, it blasts it with a jolt of electricity. If you come across a blackened berry, it's evidence that this Pokémon mistook the intensity of its charge. ",
        "The leaves growing on Sceptile's body are very sharp edged. This Pokémon is very agile—it leaps all over the branches of trees and jumps on its foe from above or behind. ",
        "Swampert is very strong. It has enough power to easily drag a boulder weighing more than a ton. This Pokémon also has powerful vision that lets it see even in murky water. ",
        "There is a large flower on Venusaur's back. The flower is said to take on vivid colors if it gets plenty of nutrition and sunlight. The flower's aroma soothes the emotions of people. "};


        String[] types = {"Water","Fire","Grass","Electric","Fighting","Flying","Psychic","Dark","Ground","Poison","Nan"};
        String[] colors = {"#6890F0","#F08030","#78C850","#F8D030","#D67873","#6D5E9C","#A13959","#49392F","#E0C068","#A040A0","#ffffff"};
        for (int i=0; i<names.length; i++)
        {
            nameToInt.put(names[i], i);
            intToType1.put(i, type1[i]);
            intToType2.put(i, type2[i]);
            intToData.put(i, data[i]);
        }

        for (int i=0; i<types.length; i++)
        {
            typeColor.put(types[i],colors[i]);
        }
    }
}
