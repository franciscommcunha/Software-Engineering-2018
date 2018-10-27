package com.github.adminfaces.starter.bean;

import com.github.adminfaces.starter.infra.model.Filter;
import com.github.adminfaces.starter.service.Data;
import com.github.adminfaces.starter.tables.Humidity;
import com.github.adminfaces.template.exception.BusinessException;
import java.io.IOException;
import org.omnifaces.cdi.ViewScoped;
import org.primefaces.model.LazyDataModel;
import org.primefaces.model.SortOrder;

import javax.annotation.PostConstruct;
import javax.inject.Inject;
import javax.inject.Named;
import java.io.Serializable;
import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

@Named
@ViewScoped
public class HumListMB implements Serializable {

    @Inject
    Data data;

    Integer id;

    LazyDataModel<Humidity> hums;

    Filter<Humidity> filter = new Filter<>(new Humidity());

    List<Humidity> selectedTemps;

    List<Humidity> filteredValue;// datatable filteredValue attribute (column filters)

    @PostConstruct
    public void initDataModel() {
        hums = new LazyDataModel<Humidity>() {
            @Override
            public List<Humidity> load(int first, int pageSize,
                                  String sortField, SortOrder sortOrder,
                                  Map<String, Object> filters) {
                com.github.adminfaces.starter.infra.model.SortOrder order = null;
                if (sortOrder != null) {
                    order = sortOrder.equals(SortOrder.ASCENDING) ? com.github.adminfaces.starter.infra.model.SortOrder.ASCENDING
                            : sortOrder.equals(SortOrder.DESCENDING) ? com.github.adminfaces.starter.infra.model.SortOrder.DESCENDING
                            : com.github.adminfaces.starter.infra.model.SortOrder.UNSORTED;
                }
                filter.setFirst(first).setPageSize(pageSize)
                        .setSortField(sortField).setSortOrder(order)
                        .setParams(filters);
                List<Humidity> list = null;
                try {
                    list = (List<Humidity>) data.selectHumByRoom(sortField);
                } catch (ClassNotFoundException ex) {}
                return list;
            }

            @Override
            public int getRowCount() {
                return super.getRowCount();
            }

            @Override
            public Humidity getRowData(String key){
                try {
                    return data.selectHumByRoom(key);
                } catch (ClassNotFoundException ex) {
                    Logger.getLogger(TempListMB.class.getName()).log(Level.SEVERE, null, ex);
                }
                return null;
            }
        };
    }

    public void clear() {
        filter = new Filter<>(new Humidity());
    }

    public List<Humidity> completeModel(String query) throws ClassNotFoundException, IOException {
        List<Humidity> result = data.getHumidity();
        return result;
    }

    public void findCarById(Integer id) throws ClassNotFoundException {
        if (id == null) {
            throw new BusinessException("Provide Car ID to load");
        }
        selectedTemps.add((Humidity) data.selectHumByRoom(id.toString()));
    }

    public List<Humidity> getSelectedCars() {
        return selectedTemps;
    }

    public List<Humidity> getFilteredValue() {
        return filteredValue;
    }

    public void setFilteredValue(List<Humidity> filteredValue) {
        this.filteredValue = filteredValue;
    }

    public void setSelectedCars(List<Humidity> selectedCars) {
        this.selectedTemps = selectedCars;
    }

    public LazyDataModel<Humidity> getCars() {
        return hums;
    }

    public void setCars(LazyDataModel<Humidity> cars) {
        this.hums = cars;
    }

    public Filter<Humidity> getFilter() {
        return filter;
    }

    public void setFilter(Filter<Humidity> filter) {
        this.filter = filter;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }
}