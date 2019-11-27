package com.example.pokedex.ui.main;

import android.animation.Animator;
import android.animation.ValueAnimator;
import android.app.Activity;
import android.arch.lifecycle.ViewModelProviders;
import android.content.Context;
import android.content.Intent;
import android.content.res.AssetFileDescriptor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.graphics.Matrix;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.media.ExifInterface;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.v4.app.Fragment;
import android.support.v4.content.FileProvider;
import android.view.LayoutInflater;
import android.view.Surface;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.example.pokedex.R;

import org.tensorflow.lite.Interpreter;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.lang.reflect.Array;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.util.ArrayList;
import java.util.List;


public class Camera extends Fragment {

    static final int REQUEST_TAKE_PHOTO = 1;
    private PageViewModel argument;

    private View view;
    private ImageView photo;
    private TextView pokemon;
    private TextView type1, type2;
    private ImageButton capture;
    String currentPhotoPath;
    Info info;
    private Classifier classifier;
    LinearLayout llmain;
    LinearLayout llexpand;
    TextView standby;

    public Camera() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @return A new instance of fragment Camera.
     */
    // TODO: Rename and change types and number of parameters
    public static Camera newInstance() {
        Camera fragment = new Camera();
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        argument = ViewModelProviders.of(getActivity()).get(PageViewModel.class);
        argument.setIndex(-1);
        info = new Info();
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        setPic();
//        Bitmap bitmap = (Bitmap) data.getExtras().get("data");
//        photo.setImageBitmap(bitmap);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        view = inflater.inflate(R.layout.fragment_camera, container, false);
        photo = view.findViewById(R.id.camera);
        pokemon = view.findViewById(R.id.name);
        type1 = view.findViewById(R.id.type1);
        type2 = view.findViewById(R.id.type2);
        capture = view.findViewById(R.id.capture);
        llmain = view.findViewById(R.id.main);
        llexpand = view.findViewById(R.id.expand);
        llexpand.setVisibility(View.GONE);
        standby = view.findViewById(R.id.standby);

        llmain.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (llexpand.getVisibility()==View.GONE){
                    expand();
                    standby.setVisibility(View.GONE);
                }else{
                    collapse();
                    standby.setVisibility(View.VISIBLE);
                }
            }
        });


        capture.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                // Ensure that there's a camera activity to handle the intent
                if (takePictureIntent.resolveActivity(getActivity().getPackageManager()) != null) {
                    // Create the File where the photo should go
                    File photoFile = null;
                    try {
                        photoFile = createImageFile();
                    } catch (IOException ex) {
                        // Error occurred while creating the File
                        ex.printStackTrace();
                    }
                    // Continue only if the File was successfully created
                    if (photoFile != null) {
                        Uri photoURI = FileProvider.getUriForFile(getActivity(),
                                "com.example.android.fileprovider",
                                photoFile);
                        takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI);
                        startActivityForResult(takePictureIntent, REQUEST_TAKE_PHOTO);
                    }

                }

            }
        });

        try {
            classifier = Classifier.create(getActivity());
        } catch (IOException e) {
            System.out.println("Cannot create classifier");
            e.printStackTrace();
        }
        return view;
    }


    private File createImageFile() throws IOException {
        // Create an image file name
        String imageFileName = "POKEMON_";
        File storageDir = getActivity().getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        File image = File.createTempFile(
                imageFileName,  /* prefix */
                ".jpg",         /* suffix */
                storageDir      /* directory */
        );

        // Save a file: path for use with ACTION_VIEW intents
        currentPhotoPath = image.getAbsolutePath();
        return image;
    }


    private void setPic() {
        // Get the dimensions of the View
        int targetW = photo.getWidth();
        int targetH = photo.getHeight();

        // Get the dimensions of the bitmap
        BitmapFactory.Options bmOptions = new BitmapFactory.Options();
        bmOptions.inJustDecodeBounds = true;

        int photoW = bmOptions.outWidth;
        int photoH = bmOptions.outHeight;

        // Determine how much to scale down the image
        int scaleFactor = Math.min(photoW/targetW, photoH/targetH);

        // Decode the image file into a Bitmap sized to fill the View
        bmOptions.inJustDecodeBounds = false;
        bmOptions.inSampleSize = scaleFactor;
        bmOptions.inPurgeable = true;

        Bitmap bitmap = BitmapFactory.decodeFile(currentPhotoPath, bmOptions);
        try {
            bitmap = modifyOrientation(bitmap, currentPhotoPath);
        }catch(IOException e) {
            e.printStackTrace();
        }

        photo.setImageBitmap(bitmap);

//
//        int sensor_orientation = 90 - getScreenOrientation();
        System.out.println(bitmap);
        List<Classifier.Recognition> results =
                classifier.recognizeImage(bitmap, 0);

        String pokemon_name = results.get(0).getTitle() + " _ " + results.get(0).getConfidence();
        //pokemon.setText(pokemon_name);
        getPokemon(results.get(0).getTitle());
    }


    public static Bitmap modifyOrientation(Bitmap bitmap, String image_absolute_path) throws IOException {
        ExifInterface ei = new ExifInterface(image_absolute_path);
        int orientation = ei.getAttributeInt(ExifInterface.TAG_ORIENTATION, ExifInterface.ORIENTATION_NORMAL);

        switch (orientation) {
            case ExifInterface.ORIENTATION_ROTATE_90:
                return rotate(bitmap, 90);

            case ExifInterface.ORIENTATION_ROTATE_180:
                return rotate(bitmap, 180);

            case ExifInterface.ORIENTATION_ROTATE_270:
                return rotate(bitmap, 270);

            case ExifInterface.ORIENTATION_FLIP_HORIZONTAL:
                return flip(bitmap, true, false);

            case ExifInterface.ORIENTATION_FLIP_VERTICAL:
                return flip(bitmap, false, true);

            default:
                return bitmap;
        }
    }


//    protected int getScreenOrientation() {
//        switch (getActivity().getWindowManager().getDefaultDisplay().getRotation()) {
//            case Surface.ROTATION_270:
//                return 270;
//            case Surface.ROTATION_180:
//                return 180;
//            case Surface.ROTATION_90:
//                return 90;
//            default:
//                return 0;
//        }
//    }

    public static Bitmap rotate(Bitmap bitmap, float degrees) {
        Matrix matrix = new Matrix();
        matrix.postRotate(degrees);
        return Bitmap.createBitmap(bitmap, 0, 0, bitmap.getWidth(), bitmap.getHeight(), matrix, true);
    }

    public static Bitmap flip(Bitmap bitmap, boolean horizontal, boolean vertical) {
        Matrix matrix = new Matrix();
        matrix.preScale(horizontal ? -1 : 1, vertical ? -1 : 1);
        return Bitmap.createBitmap(bitmap, 0, 0, bitmap.getWidth(), bitmap.getHeight(), matrix, true);
    }


    public void getPokemon(String pokemon_name)
    {
        // get pokemon name from image
        pokemon.setText(pokemon_name);
        int index = info.nameToInt.get(pokemon_name);
        type1.setText(info.intToType1.get(index));
        type2.setText(info.intToType2.get(index));

        try {
//            System.out.println(info.typeColor.get(info.intToType1.get(index)));
//            System.out.println(info.typeColor.get(info.intToType2.get(index)));
            type1.setBackgroundColor(Color.parseColor(info.typeColor.get(info.intToType1.get(index))));
            type2.setBackgroundColor(Color.parseColor(info.typeColor.get(info.intToType2.get(index))));
        }catch(Exception e)
        {
            e.printStackTrace();
            type1.setBackgroundColor(Color.parseColor("#ffffff"));
            type2.setBackgroundColor(Color.parseColor("#ffffff"));
        }

        argument.setIndex(index);
    }



    private void expand() {
        //set Visible
        llexpand.setVisibility(View.VISIBLE);

        final int widthSpec = View.MeasureSpec.makeMeasureSpec(0, View.MeasureSpec.UNSPECIFIED);
        final int heightSpec = View.MeasureSpec.makeMeasureSpec(0, View.MeasureSpec.UNSPECIFIED);
        llexpand.measure(widthSpec, heightSpec);

        ValueAnimator mAnimator = slideAnimator(0, llexpand.getMeasuredHeight()).setDuration(500);
        mAnimator.start();
    }

    private void collapse() {
        int finalHeight = llexpand.getHeight();

        ValueAnimator mAnimator = slideAnimator(finalHeight, 0).setDuration(500);
        mAnimator.addListener(new Animator.AnimatorListener() {
            @Override
            public void onAnimationEnd(Animator animator) {
                //Height=0, but it set visibility to GONE
                llexpand.setVisibility(View.GONE);
            }


            @Override
            public void onAnimationStart(Animator animator) {
            }

            @Override
            public void onAnimationCancel(Animator animator) {
            }

            @Override
            public void onAnimationRepeat(Animator animator) {
            }
        });
        mAnimator.start();
    }

    private ValueAnimator slideAnimator(int start, int end) {

        ValueAnimator animator = ValueAnimator.ofInt(start, end);

        animator.addUpdateListener(new ValueAnimator.AnimatorUpdateListener() {
            @Override
            public void onAnimationUpdate(ValueAnimator valueAnimator) {
                //Update Height
                int value = (Integer) valueAnimator.getAnimatedValue();
                ViewGroup.LayoutParams layoutParams = llexpand.getLayoutParams();
                layoutParams.height = value;
                llexpand.setLayoutParams(layoutParams);
            }
        });
        return animator;
    }

}
