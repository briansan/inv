package edu.villanova.ece.inv.fragment;

import android.app.Activity;
import android.content.Context;
import android.os.Bundle;
import android.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AbsListView;
import android.widget.AdapterView;
import android.widget.ListAdapter;
import android.widget.SearchView;

import java.lang.reflect.Array;
import java.util.ArrayList;

import edu.villanova.ece.inv.R;

import edu.villanova.ece.inv.adapter.AssetArrayAdapter;
import edu.villanova.ece.inv.model.Asset;
import edu.villanova.ece.inv.manager.DataManager;
import edu.villanova.ece.inv.model.Item;
import edu.villanova.ece.inv.model.Location;
import edu.villanova.ece.inv.model.User;
import com.breadtech.util.StringUtil;

/**
 * A fragment representing a list of Items.
 * <p/>
 * Large screen devices (such as tablets) are supported by replacing the ListView
 * with a GridView.
 * <p/>
 * Activities containing this fragment MUST implement the {@link Delegate}
 * interface.
 */
public class AssetListFragment extends Fragment implements AbsListView.OnItemClickListener {

    private SearchView searchBar;
    private Delegate mListener;
    private ArrayList<Asset> assets, displayedAssets;
    private Object ref;

    /**
     * The fragment's ListView/GridView.
     */
    private AbsListView mListView;

    /**
     * The Adapter which will be used to populate the ListView/GridView with
     * Views.
     */
    private ListAdapter mAdapter;

    public static AssetListFragment newInstance(Location loc) {
        AssetListFragment fragment = new AssetListFragment();
        fragment.ref = loc;
        return fragment;
    }
    public static AssetListFragment newInstance(User loc) {
        AssetListFragment fragment = new AssetListFragment();
        fragment.ref = loc;
        return fragment;
    }
    public static AssetListFragment newInstance(Item loc) {
        AssetListFragment fragment = new AssetListFragment();
        fragment.ref = loc;
        return fragment;
    }
    public static AssetListFragment newInstance(String loc) {
        if (loc == null) return newInstance();
        AssetListFragment fragment = new AssetListFragment();
        fragment.ref = loc;
        return fragment;
    }
    public static AssetListFragment newInstance() {
        AssetListFragment fragment = new AssetListFragment();
        fragment.ref = new Object();
        return fragment;
    }

    /**
     * Mandatory empty constructor for the fragment manager to instantiate the
     * fragment (e.g. upon screen orientation changes).
     */
    public AssetListFragment() {}

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        if (ref == null) {
            assets = DataManager.sharedManager().getAssets();
        } else if (ref.getClass() == Location.class) {
            assets = DataManager.sharedManager().getLocationAssetMap().get(this.ref);
        } else if (ref.getClass() == Item.class) {
            assets = DataManager.sharedManager().getItemAssetMap().get(this.ref);
        } else if (ref.getClass() == User.class) {
            assets = DataManager.sharedManager().getUserAssetMap().get(this.ref);
        } else if (ref.getClass() == String.class){
            ArrayList<Asset> assets = DataManager.sharedManager().getAssets();
            this.assets = new ArrayList();
            for (Asset a : assets) {
                if (a.getTag_ece().contains(this.ref.toString())) {
                    this.assets.add(a);
                }
            }
        } else {
            assets = DataManager.sharedManager().getAssets();
        }
        mAdapter = new AssetArrayAdapter(this.getActivity(),R.layout.list_item_no_img,assets);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_list_search, container, false);

        // Set the adapter
        mListView = (AbsListView) view.findViewById(android.R.id.list);
        ((AdapterView<ListAdapter>) mListView).setAdapter(mAdapter);
        searchBar = (SearchView)view.findViewById(R.id.searchBar);

        // Set OnItemClickListener so we can be notified on item clicks
        mListView.setOnItemClickListener(this);
        searchBar.setOnQueryTextListener(new SearchView.OnQueryTextListener() {
            @Override
            public boolean onQueryTextSubmit(String query) {
                return onQueryTextChange(query);
            }

            @Override
            public boolean onQueryTextChange(String newText) {
                ArrayList<Asset> newAssets = new ArrayList<Asset>();
                for (Asset a : assets) {
                    boolean ece_match = StringUtil.containsIgnoreCase(a.getTag_ece(), newText);
                    boolean item_match = StringUtil.containsIgnoreCase(a.getItem().toString(),newText);
                    boolean location_match = StringUtil.containsIgnoreCase(a.getHome().toString(),newText) ||
                            StringUtil.containsIgnoreCase(a.getCurrent().toString(),newText);
                    boolean user_match = StringUtil.containsIgnoreCase(a.getOwner().toString(),newText) ||
                            StringUtil.containsIgnoreCase(a.getHolder().toString(),newText);
                    if (ece_match || item_match || location_match || user_match) {
                        newAssets.add(a);
                    }
                }
                displayedAssets = newText.length() > 0 ? newAssets : assets;
                mListView.setAdapter(new AssetArrayAdapter(getActivity(),R.layout.list_item_no_img,displayedAssets));
                return true;
            }
        });

        return view;
    }

    @Override
    public void onAttach(Context activity) {
        super.onAttach(activity);
        try {
            mListener = (Delegate) activity;
        } catch (ClassCastException e) {
            throw new ClassCastException(activity.toString()
                    + " must implement didSelectItem");
        }
    }

    @Override
    public void onDetach() {
        super.onDetach();
        mListener = null;
    }

    @Override
    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
        if (null != mListener) {
            // Notify the active callbacks interface (the activity, if the
            // fragment is attached to one) that an item has been selected.
            Asset cat = displayedAssets != null ? displayedAssets.get(position) : assets.get(position);
            mListener.didSelectAsset(cat);
        }
    }

    /**
     * This interface must be implemented by activities that contain this
     * fragment to allow an interaction in this fragment to be communicated
     * to the activity and potentially other fragments contained in that
     * activity.
     * <p/>
     * See the Android Training lesson <a href=
     * "http://developer.android.com/training/basics/fragments/communicating.html"
     * >Communicating with Other Fragments</a> for more information.
     */
    public interface Delegate {
        public void didSelectAsset( Asset item);
    }

}
