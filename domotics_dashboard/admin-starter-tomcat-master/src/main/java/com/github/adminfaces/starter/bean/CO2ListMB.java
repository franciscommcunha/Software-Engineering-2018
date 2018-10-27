package com.github.adminfaces.starter.bean;

import com.github.adminfaces.starter.infra.model.Filter;
import com.github.adminfaces.starter.service.Data;
import com.github.adminfaces.starter.tables.CO2;
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
public class CO2ListMB implements Serializable {

    @Inject
    Data data;

    Integer id;

    LazyDataModel<CO2> hums;

    Filter<CO2> filter = new Filter<>(new CO2());

    List<CO2> selectedTemps;

    List<CO2> filteredValue;// datatable filteredValue attribute (column filters)

    @PostConstruct
    public void initDataModel() {
        hums = new LazyDataModel<CO2>() {
            @Override
            public List<CO2> load(int first, int pageSize,
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
                List<CO2> list = null;
                try {
                    list = (List<CO2>) data.selectCO2ById(sortField);
                } catch (ClassNotFoundException ex) {}
                return list;
            }

            @Override
            public int getRowCount() {
                return super.getRowCount();
            }

            @Override
            public CO2 getRowData(String key){
                try {
                    return data.selectCO2ById(key);
                } catch (ClassNotFoundException ex) {
                    Logger.getLogger(TempListMB.class.getName()).log(Level.SEVERE, null, ex);
                }
                return null;
            }
        };
    }

    public void clear() {
        filter = new Filter<>(new CO2());
    }

    public List<CO2> completeModel(String query) throws ClassNotFoundException, IOException {
        List<CO2> result = data.getCO2();
        return result;
    }

    public void findCarById(Integer id) throws ClassNotFoundException {
        if (id == null) {
            throw new BusinessException("Provide Car ID to load");
        }
        selectedTemps.add((CO2) data.selectCO2ById(id.toString()));
    }

    public List<CO2> getSelectedCars() {
        return selectedTemps;
    }

    public List<CO2> getFilteredValue() {
        return filteredValue;
    }

    public void setFilteredValue(List<CO2> filteredValue) {
        this.filteredValue = filteredValue;
    }

    public void setSelectedCars(List<CO2> selectedCars) {
        this.selectedTemps = selectedCars;
    }

    public LazyDataModel<CO2> getCars() {
        return hums;
    }

    public void setCars(LazyDataModel<CO2> cars) {
        this.hums = cars;
    }

    public Filter<CO2> getFilter() {
        return filter;
    }

    public void setFilter(Filter<CO2> filter) {
        this.filter = filter;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }
}