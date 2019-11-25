package com.example.pokedex.ui.main;

import android.arch.lifecycle.Observer;
import android.arch.lifecycle.ViewModelProviders;
import android.content.Context;
import android.net.Uri;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.example.pokedex.R;


public class Data extends Fragment {
    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String charizard = "It spits fire that is hot enough to melt boulders. It may cause forest fires by blowing flames.";
    private static Integer value = -1;
    // TODO: Rename and change types of parameters
    private String name_pok_private;
    private TextView tv;
    private PageViewModel argument;

    public Data() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @return A new instance of fragment Data.
     */
    // TODO: Rename and change types and number of parameters
    public static Data newInstance(String name_pok) {
        Data fragment = new Data();
        Bundle args = new Bundle();
        args.putString(ARG_PARAM1, name_pok);
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
            name_pok_private = getArguments().getString(ARG_PARAM1);
        }

        argument = ViewModelProviders.of(getActivity()).get(PageViewModel.class);


    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view = inflater.inflate(R.layout.fragment_data, container, false);
        tv = view.findViewById(R.id.data);
        PageViewModel argument = ViewModelProviders.of(getActivity()).get(PageViewModel.class);
        argument.getIndex().observe(this, new Observer<Integer>() {
            @Override
            public void onChanged(@Nullable Integer s) {
                value = s;
                tv.setText(String.valueOf(s));
            }
        });


        return view;
    }

}
