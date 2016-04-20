package edu.villanova.ece.inv.fragment;

import android.app.Activity;
import android.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AbsListView;
import android.widget.AdapterView;
import android.widget.ListAdapter;

import java.util.ArrayList;

import edu.villanova.ece.inv.R;
import edu.villanova.ece.inv.adapter.InvArrayAdapter;
import edu.villanova.ece.inv.model.Asset;
import edu.villanova.ece.inv.manager.DataManager;
import edu.villanova.ece.inv.model.Inventory;
import edu.villanova.ece.inv.model.User;

/**
 * A fragment representing a list of Items.
 * <p/>
 * Large screen devices (such as tablets) are supported by replacing the ListView
 * with a GridView.
 * <p/>
 * Activities containing this fragment MUST implement the {@link Delegate}
 * interface.
 */
public class InvListFragment extends Fragment implements AbsListView.OnItemClickListener {


    private Delegate mListener;
    private ArrayList<Inventory> invs;
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

    public static InvListFragment newInstance(Asset loc) {
        InvListFragment fragment = new InvListFragment();
        fragment.ref = loc;
        return fragment;
    }
    public static InvListFragment newInstance(User loc) {
        InvListFragment fragment = new InvListFragment();
        fragment.ref = loc;
        return fragment;
    }
    public static InvListFragment newInstance() {
        InvListFragment fragment = new InvListFragment();
        fragment.ref = new Object();
        return fragment;
    }

    /**
     * Mandatory empty constructor for the fragment manager to instantiate the
     * fragment (e.g. upon screen orientation changes).
     */
    public InvListFragment() {}

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        if (ref != null) {
            if (ref.getClass() == Asset.class) {
                invs = DataManager.sharedManager().getAssetInvMap().get(this.ref);
            } else if (ref.getClass() == User.class) {
                invs = DataManager.sharedManager().getUserInvMap().get(this.ref);
            } else {
                invs = DataManager.sharedManager().getInvs();
            }
        }
        mAdapter = new InvArrayAdapter(this.getActivity(),R.layout.list_item_no_img,invs);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_list, container, false);

        // Set the adapter
        mListView = (AbsListView) view.findViewById(android.R.id.list);
        ((AdapterView<ListAdapter>) mListView).setAdapter(mAdapter);

        // Set OnItemClickListener so we can be notified on item clicks
        mListView.setOnItemClickListener(this);

        return view;
    }

    @Override
    public void onAttach(Activity activity) {
        super.onAttach(activity);
        try {
            mListener = (Delegate) activity;
        } catch (ClassCastException e) {
            throw new ClassCastException(activity.toString()
                    + " must implement didSelectInv");
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
            Inventory cat = invs.get(position);
            mListener.didSelectInv(cat);
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
        public void didSelectInv(Inventory item);
    }

}
