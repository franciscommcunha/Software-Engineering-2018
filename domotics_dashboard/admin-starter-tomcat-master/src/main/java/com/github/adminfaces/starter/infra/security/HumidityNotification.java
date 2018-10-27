package com.github.adminfaces.starter.infra.security;

import org.omnifaces.util.Faces;
import javax.enterprise.inject.Specializes;
import javax.faces.context.FacesContext;
import javax.inject.Named;
import java.io.IOException;
import java.io.Serializable;
import static com.github.adminfaces.starter.util.Utils.addDetailMessage;
import javax.enterprise.context.SessionScoped;
import org.omnifaces.cdi.ViewScoped;

/**
 *
 * @author raquelramos
 */

@Named
@ViewScoped
public class HumidityNotification implements Serializable {

    public static void humidityHigh() throws IOException {
        addDetailMessage("Humidity values are too <b>high</b>. Dehumidifier will be turned on.");
        Faces.getExternalContext().getFlash().setKeepMessages(true);
        //Faces.redirect("index.xhtml");
    }
    
    public static void humidityLow() throws IOException {
        addDetailMessage("Humidity values are too <b>low</b>. Dehumidifier will be turned off.");
        Faces.getExternalContext().getFlash().setKeepMessages(true);
        //Faces.redirect("index.xhtml");
    }
}

