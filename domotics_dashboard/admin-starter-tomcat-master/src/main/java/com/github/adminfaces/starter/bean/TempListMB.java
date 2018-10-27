package com.github.adminfaces.starter.bean;

import com.github.adminfaces.starter.infra.model.Filter;
import com.github.adminfaces.starter.tables.Temperature;
import com.github.adminfaces.starter.service.Data;
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
public class TempListMB implements Serializable {

    @Inject
    Data data;

    Integer id;

    LazyDataModel<Temperature> temperatures;

    Filter<Temperature> filter = new Filter<>(new Temperature());

    List<Temperature> selectedTemps;

    List<Temperature> filteredValue;// datatable filteredValue attribute (column filters)

    @PostConstruct
    public void initDataModel() {
        temperatures = new LazyDataModel<Temperature>() {
            @Override
            public List<Temperature> load(int first, int pageSize,
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
                List<Temperature> list = null;
                try {
                    list = (List<Temperature>) data.selectTempByRoom(sortField);
                } catch (ClassNotFoundException ex) {}
                return list;
            }

            @Override
            public int getRowCount() {
                return super.getRowCount();
            }

            @Override
            public Temperature getRowData(String key){
                try {
                    return data.selectTempByRoom(key);
                } catch (ClassNotFoundException ex) {
                    Logger.getLogger(TempListMB.class.getName()).log(Level.SEVERE, null, ex);
                }
                return null;
            }
        };
    }

    public void clear() {
        filter = new Filter<>(new Temperature());
    }

    public List<Temperature> completeModel(String query) throws ClassNotFoundException, IOException {
        List<Temperature> result = data.getTemperatures();
        return result;
    }

    public void findCarById(Integer id) throws ClassNotFoundException {
        if (id == null) {
            throw new BusinessException("Provide Car ID to load");
        }
        selectedTemps.add((Temperature) data.selectTempByRoom(id.toString()));
    }

    public List<Temperature> getSelectedCars() {
        return selectedTemps;
    }

    public List<Temperature> getFilteredValue() {
        return filteredValue;
    }

    public void setFilteredValue(List<Temperature> filteredValue) {
        this.filteredValue = filteredValue;
    }

    public void setSelectedCars(List<Temperature> selectedCars) {
        this.selectedTemps = selectedCars;
    }

    public LazyDataModel<Temperature> getCars() {
        return temperatures;
    }

    public void setCars(LazyDataModel<Temperature> cars) {
        this.temperatures = cars;
    }

    public Filter<Temperature> getFilter() {
        return filter;
    }

    public void setFilter(Filter<Temperature> filter) {
        this.filter = filter;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }
}