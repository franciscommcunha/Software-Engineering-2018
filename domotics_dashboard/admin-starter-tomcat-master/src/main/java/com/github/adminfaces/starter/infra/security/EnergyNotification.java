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
public class EnergyNotification implements Serializable {

    public static void energyHigh() throws IOException {
        addDetailMessage("The consume of energy by your house appliances is too <b>high</b>. "
                + "Some appliances will be turned off.");
        Faces.getExternalContext().getFlash().setKeepMessages(true);
        //Faces.redirect("index.xhtml");
    }
}

